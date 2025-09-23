# Personal Day Planner API - Postman Testing Guide

## Base URL
```
http://localhost:8000
```

## Authentication
No authentication required (for now)

---

## 1. Health Check Endpoints

### Get Root Information
```
GET http://localhost:8000/
```

### Health Check
```
GET http://localhost:8000/health
```

---

## 2. Task Management Endpoints

### Create Task
```
POST http://localhost:8000/tasks
Content-Type: application/json

{
  "title": "Complete project documentation",
  "description": "Write comprehensive documentation for the personal day planner project",
  "priority": 75.5,
  "completed": false,
  "paused": false,
  "due_date": "2025-09-25T10:00:00"
}
```

**Sample Payloads:**

High Priority Task:
```json
{
  "title": "Fix critical bug",
  "description": "Resolve the database connection issue",
  "priority": 90.0,
  "completed": false,
  "paused": false,
  "due_date": "2025-09-23T09:00:00"
}
```

Medium Priority Task:
```json
{
  "title": "Review code changes",
  "description": "Review the recent pull requests",
  "priority": 50.0,
  "completed": false,
  "paused": false
}
```

Low Priority Task:
```json
{
  "title": "Update team calendar",
  "description": "Add upcoming meetings to the shared calendar",
  "priority": 25.0,
  "completed": false,
  "paused": false,
  "due_date": "2025-09-30T17:00:00"
}
```

### Get All Tasks
```
GET http://localhost:8000/tasks
```

### Get Task by ID
```
GET http://localhost:8000/tasks/{task_id}
```

Example:
```
GET http://localhost:8000/tasks/6729a1b2c3d4e5f6789012ab
```

### Update Task
```
PUT http://localhost:8000/tasks/{task_id}
Content-Type: application/json

{
  "title": "Updated task title",
  "description": "Updated description",
  "priority": 85.0,
  "completed": true,
  "paused": false,
  "due_date": "2025-09-26T15:30:00"
}
```

**Sample Update Payloads:**

Mark as Completed:
```json
{
  "completed": true
}
```

Change Priority:
```json
{
  "priority": 95.0
}
```

Pause Task:
```json
{
  "paused": true
}
```

Update Multiple Fields:
```json
{
  "title": "Refactored task title",
  "priority": 60.0,
  "completed": false,
  "paused": false,
  "description": "Updated task with new requirements"
}
```

### Delete Task
```
DELETE http://localhost:8000/tasks/{task_id}
```

Example:
```
DELETE http://localhost:8000/tasks/6729a1b2c3d4e5f6789012ab
```

---

## 3. Filter Endpoints

### Get Tasks by Priority Range
```
GET http://localhost:8000/tasks/priority/{min_priority}/{max_priority}
```

Examples:
```
GET http://localhost:8000/tasks/priority/80/100
GET http://localhost:8000/tasks/priority/50/75
GET http://localhost:8000/tasks/priority/0/25
```

### Get Tasks by Completion Status
```
GET http://localhost:8000/tasks/status/{completed}
```

Examples:
```
GET http://localhost:8000/tasks/status/true
GET http://localhost:8000/tasks/status/false
```

### Get Tasks by Paused Status
```
GET http://localhost:8000/tasks/paused/{paused}
```

Examples:
```
GET http://localhost:8000/tasks/paused/true
GET http://localhost:8000/tasks/paused/false
```

---

## 4. Testing Scenarios

### Scenario 1: Create and Manage a Task
1. **Create a new task:**
   ```
   POST http://localhost:8000/tasks
   
   {
     "title": "Learn FastAPI",
     "description": "Complete FastAPI tutorial and build a sample project",
     "priority": 80.0,
     "completed": false,
     "paused": false,
     "due_date": "2025-09-28T18:00:00"
   }
   ```

2. **Get all tasks to see the created task:**
   ```
   GET http://localhost:8000/tasks
   ```

3. **Update the task (mark as started):**
   ```
   PUT http://localhost:8000/tasks/{task_id}
   
   {
     "description": "Currently working on FastAPI tutorial - 50% complete"
   }
   ```

4. **Pause the task:**
   ```
   PUT http://localhost:8000/tasks/{task_id}
   
   {
     "paused": true
   }
   ```

5. **Resume and complete the task:**
   ```
   PUT http://localhost:8000/tasks/{task_id}
   
   {
     "paused": false,
     "completed": true,
     "priority": 100.0
   }
   ```

### Scenario 2: Priority Management
1. **Create high priority task:**
   ```
   POST http://localhost:8000/tasks
   
   {
     "title": "Emergency server maintenance",
     "priority": 95.0,
     "due_date": "2025-09-22T20:00:00"
   }
   ```

2. **Create medium priority task:**
   ```
   POST http://localhost:8000/tasks
   
   {
     "title": "Weekly team meeting preparation",
     "priority": 60.0,
     "due_date": "2025-09-24T09:00:00"
   }
   ```

3. **Create low priority task:**
   ```
   POST http://localhost:8000/tasks
   
   {
     "title": "Organize desktop files",
     "priority": 20.0
   }
   ```

4. **Filter high priority tasks:**
   ```
   GET http://localhost:8000/tasks/priority/80/100
   ```

### Scenario 3: Error Testing
1. **Try invalid priority (should fail):**
   ```
   POST http://localhost:8000/tasks
   
   {
     "title": "Invalid priority task",
     "priority": 150.0
   }
   ```

2. **Try to get non-existent task:**
   ```
   GET http://localhost:8000/tasks/invalid-task-id
   ```

3. **Try to update non-existent task:**
   ```
   PUT http://localhost:8000/tasks/invalid-task-id
   
   {
     "title": "This should fail"
   }
   ```

---

## 5. Expected Response Formats

### Successful Task Creation Response:
```json
{
  "id": "6729a1b2c3d4e5f6789012ab",
  "title": "Complete project documentation",
  "description": "Write comprehensive documentation for the personal day planner project",
  "priority": 75.5,
  "completed": false,
  "paused": false,
  "created_at": "2025-09-22T14:30:00.123456",
  "updated_at": "2025-09-22T14:30:00.123456",
  "due_date": "2025-09-25T10:00:00"
}
```

### Task List Response:
```json
[
  {
    "id": "6729a1b2c3d4e5f6789012ab",
    "title": "Complete project documentation",
    "description": "Write comprehensive documentation",
    "priority": 75.5,
    "completed": false,
    "paused": false,
    "created_at": "2025-09-22T14:30:00.123456",
    "updated_at": "2025-09-22T14:30:00.123456",
    "due_date": "2025-09-25T10:00:00"
  }
]
```

### Error Response:
```json
{
  "detail": "Priority must be between 0 and 100"
}
```

---

## 6. Quick Test Collection for Postman

### Import these as a Postman Collection:

1. **Health Check** - GET `{{base_url}}/health`
2. **Create Task** - POST `{{base_url}}/tasks` with sample payload
3. **Get All Tasks** - GET `{{base_url}}/tasks`
4. **Get Task by ID** - GET `{{base_url}}/tasks/{{task_id}}`
5. **Update Task** - PUT `{{base_url}}/tasks/{{task_id}}` with update payload
6. **Delete Task** - DELETE `{{base_url}}/tasks/{{task_id}}`
7. **High Priority Tasks** - GET `{{base_url}}/tasks/priority/80/100`
8. **Completed Tasks** - GET `{{base_url}}/tasks/status/true`
9. **Paused Tasks** - GET `{{base_url}}/tasks/paused/true`

### Environment Variables:
- `base_url`: `http://localhost:8000`
- `task_id`: (copy from create task response)

---

## 7. Notes for Testing

- **Priority**: Must be between 0.0 and 100.0 (inclusive)
- **Dates**: Use ISO format: `"2025-09-22T14:30:00"`
- **Boolean fields**: `true` or `false` (lowercase)
- **Task ID**: Copy the `id` from create/get responses for testing specific tasks
- **Server**: Make sure the FastAPI server is running on `http://localhost:8000`

Start the server with:
```bash
cd server
source venv/Scripts/activate  # or .\venv\Scripts\activate on Windows
python run_server.py
```

---

## 8. Troubleshooting

### Database Connection Issues

If you get an error like "empty database name not allowed", make sure your `DATABASE_URL` in `.env` includes the database name:

**Correct format:**
```
DATABASE_URL=mongodb+srv://username:password@cluster.mongodb.net/database_name?retryWrites=true&w=majority
```

**Incorrect format (missing database name):**
```
DATABASE_URL=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
```

### First Time Setup
Before testing, make sure to push the schema to your database:
```bash
cd server
source venv/Scripts/activate
prisma db push
```

### Common Test Results
- **Task Creation Success**: Returns task object with generated `id` and timestamps
- **Database Connection**: Health endpoint shows task count
- **Priority Validation**: Values outside 0-100 range return 400 error