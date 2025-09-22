# Personal Day Planner - Backend API

A FastAPI-based backend for managing personal todos and tasks.

## Features

- RESTful API for todo management
- MongoDB Atlas integration
- CORS support for frontend integration
- Pydantic models for data validation
- Full CRUD operations for todos

## Setup Instructions

### 1. Set Up Virtual Environment (Recommended)

Create and activate a virtual environment to avoid dependency conflicts:

**Windows:**
```bash
cd server
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements-stable.txt
```

**Unix/Mac:**
```bash
cd server
python -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements-stable.txt
```

**Quick Setup (Windows):**
```bash
cd server
setup_venv.bat
```

### 2. Alternative: Direct Installation (Not Recommended)

If you encounter compilation errors with the main requirements file:

**Option 1: Stable requirements (Python 3.13 compatible)**
```bash
cd server
pip install -r requirements-stable.txt
```

**Option 2: Main requirements (latest versions)**
```bash
cd server
pip install -r requirements.txt
```

### 2. Configure Environment

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Update the `.env` file with your MongoDB Atlas connection string:
   ```
   MONGODB_URL=mongodb+srv://<username>:<password>@<cluster-name>.mongodb.net/<database-name>?retryWrites=true&w=majority
   ```

### 3. MongoDB Atlas Setup

1. Create a MongoDB Atlas account at https://www.mongodb.com/atlas
2. Create a new cluster
3. Create a database user with read/write permissions
4. Whitelist your IP address
5. Get the connection string and update the `.env` file

### 4. Run the Server

**With Virtual Environment (Recommended):**
```bash
# Windows
cd server
venv\Scripts\activate
python run_server.py

# Unix/Mac
cd server
source venv/bin/activate
python run_server.py
```

**Alternative Methods:**
```bash
# Using uvicorn directly (in venv)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Using the startup script
python start.py
```

The API will be available at: http://localhost:8000

### 5. API Documentation

Once the server is running, you can access:
- Interactive API docs: http://localhost:8000/docs
- ReDoc documentation: http://localhost:8000/redoc

## API Endpoints

### Todos
- `GET /todos` - Get all todos
- `POST /todos` - Create a new todo
- `GET /todos/{todo_id}` - Get a specific todo
- `PUT /todos/{todo_id}` - Update a todo
- `DELETE /todos/{todo_id}` - Delete a todo

### Health Check
- `GET /health` - Server health check
- `GET /` - Root endpoint

## Todo Model

```json
{
  "title": "string",
  "description": "string (optional)",
  "completed": "boolean (default: false)",
  "priority": "string (low/medium/high, default: medium)",
  "due_date": "string (optional, ISO format)",
  "created_at": "string (ISO format)",
  "updated_at": "string (ISO format)"
}
```

## Development

The server runs with auto-reload enabled during development. Any changes to the code will automatically restart the server.

## Production Deployment

For production deployment:
1. Set `ENVIRONMENT=production` in your `.env` file
2. Update `ALLOWED_ORIGINS` with your frontend domain
3. Use a production WSGI server like gunicorn
4. Set up proper security measures and environment variables