from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from prisma import Prisma
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

# Prisma client
db = Prisma()

# Pydantic models for API
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: float = 50.0  # Priority as percentage (0-100)
    completed: bool = False
    paused: bool = False
    due_date: Optional[datetime] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[float] = None
    completed: Optional[bool] = None
    paused: Optional[bool] = None
    due_date: Optional[datetime] = None

class TaskResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    priority: float
    completed: bool
    paused: bool
    created_at: datetime
    updated_at: datetime
    due_date: Optional[datetime] = None

# Database connection events
@app.on_event("startup")
async def startup():
    await db.connect()
    print("✅ Connected to MongoDB via Prisma")

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()
    print("👋 Disconnected from MongoDB")

# Routes
@app.get("/")
async def root():
    return {
        "message": "Personal Day Planner API", 
        "status": "running",
        "database": "MongoDB + Prisma"
    }

@app.get("/health")
async def health_check():
    try:
        # Test database connection by counting tasks
        count = await db.task.count()
        return {
            "status": "healthy", 
            "database": "connected",
            "tasks_count": count
        }
    except Exception as e:
        return {
            "status": "unhealthy", 
            "database": "disconnected", 
            "error": str(e)
        }

@app.post("/tasks", response_model=TaskResponse)
async def create_task(task: TaskCreate):
    try:
        # Validate priority is between 0 and 100
        if task.priority < 0 or task.priority > 100:
            raise HTTPException(status_code=400, detail="Priority must be between 0 and 100")
        
        created_task = await db.task.create(
            data={
                "title": task.title,
                "description": task.description,
                "priority": task.priority,
                "completed": task.completed,
                "paused": task.paused,
                "due_date": task.due_date,
            }
        )
        return created_task
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create task: {str(e)}")

@app.get("/tasks", response_model=List[TaskResponse])
async def get_all_tasks():
    try:
        tasks = await db.task.find_many(
            order={"created_at": "desc"}
        )
        return tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch tasks: {str(e)}")

@app.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task_by_id(task_id: str):
    try:
        task = await db.task.find_unique(
            where={"id": task_id}
        )
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail="Task not found")
        raise HTTPException(status_code=500, detail=f"Failed to fetch task: {str(e)}")

@app.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_id: str, task_update: TaskUpdate):
    try:
        # Build update data, only including fields that are provided
        update_data = {}
        if task_update.title is not None:
            update_data["title"] = task_update.title
        if task_update.description is not None:
            update_data["description"] = task_update.description
        if task_update.priority is not None:
            if task_update.priority < 0 or task_update.priority > 100:
                raise HTTPException(status_code=400, detail="Priority must be between 0 and 100")
            update_data["priority"] = task_update.priority
        if task_update.completed is not None:
            update_data["completed"] = task_update.completed
        if task_update.paused is not None:
            update_data["paused"] = task_update.paused
        if task_update.due_date is not None:
            update_data["due_date"] = task_update.due_date
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        updated_task = await db.task.update(
            where={"id": task_id},
            data=update_data
        )
        return updated_task
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail="Task not found")
        raise HTTPException(status_code=500, detail=f"Failed to update task: {str(e)}")

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    try:
        await db.task.delete(
            where={"id": task_id}
        )
        return {"message": "Task deleted successfully"}
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail="Task not found")
        raise HTTPException(status_code=500, detail=f"Failed to delete task: {str(e)}")

# Additional endpoints for filtering
@app.get("/tasks/priority/{min_priority}/{max_priority}", response_model=List[TaskResponse])
async def get_tasks_by_priority_range(min_priority: float, max_priority: float):
    try:
        if min_priority < 0 or max_priority > 100 or min_priority > max_priority:
            raise HTTPException(status_code=400, detail="Invalid priority range")
        
        tasks = await db.task.find_many(
            where={
                "priority": {
                    "gte": min_priority,
                    "lte": max_priority
                }
            },
            order={"priority": "desc"}
        )
        return tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch tasks: {str(e)}")

@app.get("/tasks/status/{completed}", response_model=List[TaskResponse])
async def get_tasks_by_completion_status(completed: bool):
    try:
        tasks = await db.task.find_many(
            where={"completed": completed},
            order={"created_at": "desc"}
        )
        return tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch tasks: {str(e)}")

@app.get("/tasks/paused/{paused}", response_model=List[TaskResponse])
async def get_tasks_by_paused_status(paused: bool):
    try:
        tasks = await db.task.find_many(
            where={"paused": paused},
            order={"created_at": "desc"}
        )
        return tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch tasks: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)