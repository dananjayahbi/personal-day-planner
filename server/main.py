from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional, List
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

app = FastAPI(title="Personal Day Planner API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
client = MongoClient(MONGODB_URL)
db = client.personal_day_planner
todos_collection = db.todos

# Pydantic models (compatible with both v1 and v2)
class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: Optional[str] = "medium"  # low, medium, high
    due_date: Optional[str] = None

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    due_date: Optional[str] = None

class TodoResponse(BaseModel):
    id: str = Field(alias="_id")
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: str = "medium"
    due_date: Optional[str] = None
    created_at: str
    updated_at: str

    class Config:
        allow_population_by_field_name = True
        # For Pydantic v2 compatibility
        populate_by_name = True

# Helper function to convert ObjectId to string
def todo_helper(todo) -> dict:
    return {
        "id": str(todo["_id"]),
        "title": todo["title"],
        "description": todo.get("description"),
        "completed": todo.get("completed", False),
        "priority": todo.get("priority", "medium"),
        "due_date": todo.get("due_date"),
        "created_at": todo.get("created_at"),
        "updated_at": todo.get("updated_at")
    }

# Routes
@app.get("/")
async def root():
    return {"message": "Personal Day Planner API", "status": "running"}

@app.get("/health")
async def health_check():
    try:
        # Test database connection
        client.admin.command('ping')
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}

@app.post("/todos")
async def create_todo(todo: TodoCreate):
    todo_dict = todo.dict()
    todo_dict["created_at"] = datetime.utcnow().isoformat()
    todo_dict["updated_at"] = datetime.utcnow().isoformat()
    
    result = todos_collection.insert_one(todo_dict)
    created_todo = todos_collection.find_one({"_id": result.inserted_id})
    
    return todo_helper(created_todo)

@app.get("/todos")
async def get_todos():
    todos = list(todos_collection.find())
    return [todo_helper(todo) for todo in todos]

@app.get("/todos/{todo_id}")
async def get_todo(todo_id: str):
    if not ObjectId.is_valid(todo_id):
        raise HTTPException(status_code=400, detail="Invalid todo ID format")
    
    todo = todos_collection.find_one({"_id": ObjectId(todo_id)})
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    return todo_helper(todo)

@app.put("/todos/{todo_id}")
async def update_todo(todo_id: str, todo_update: TodoUpdate):
    if not ObjectId.is_valid(todo_id):
        raise HTTPException(status_code=400, detail="Invalid todo ID format")
    
    update_data = {k: v for k, v in todo_update.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    update_data["updated_at"] = datetime.utcnow().isoformat()
    
    result = todos_collection.update_one(
        {"_id": ObjectId(todo_id)}, 
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    updated_todo = todos_collection.find_one({"_id": ObjectId(todo_id)})
    return todo_helper(updated_todo)

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: str):
    if not ObjectId.is_valid(todo_id):
        raise HTTPException(status_code=400, detail="Invalid todo ID format")
    
    result = todos_collection.delete_one({"_id": ObjectId(todo_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    return {"message": "Todo deleted successfully"}

@app.get("/todos/priority/{priority}")
async def get_todos_by_priority(priority: str):
    if priority not in ["low", "medium", "high"]:
        raise HTTPException(status_code=400, detail="Priority must be 'low', 'medium', or 'high'")
    
    todos = list(todos_collection.find({"priority": priority}))
    return [todo_helper(todo) for todo in todos]

@app.get("/todos/status/{completed}")
async def get_todos_by_status(completed: bool):
    todos = list(todos_collection.find({"completed": completed}))
    return [todo_helper(todo) for todo in todos]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)