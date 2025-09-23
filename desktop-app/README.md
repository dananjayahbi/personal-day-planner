# Personal Day Planner Desktop App

A modern task management desktop application built with tkinter that connects to the Personal Day Planner API server.

## Features

- **Modern UI Design**: Clean and intuitive interface with modern styling
- **Real-time Connection Monitoring**: App ensures constant connection to server
- **Complete Task Management**: Create, read, update, delete tasks
- **Advanced Filtering**: Filter by priority range, completion status, and paused status
- **Priority Management**: Visual priority indicators with color coding
- **Due Date Support**: Set and display task due dates
- **Status Management**: Mark tasks as completed, paused, or active
- **Responsive Design**: Scrollable interface that adapts to content

## Requirements

- Python 3.7 or higher
- tkinter (usually included with Python)
- requests library
- Personal Day Planner API server running

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure the API server is running on the configured URL (default: http://localhost:8000)

## Usage

Run the application using the consolidated version:
```bash
python task_manager.py
```

Or run the modular version:
```bash
python app.py
```

**Note**: If you encounter import issues, use `task_manager.py` which contains all components in a single file.

## Configuration

The API base URL can be changed in `config/api_config.py`:

```python
BASE_URL = "http://localhost:8000"  # Change this for production deployment
```

## Project Structure

```
desktop-app/
├── app.py                 # Main entry point
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── config/
│   └── api_config.py     # API configuration
└── src/
    ├── main.py           # Main application window
    ├── api/
    │   └── client.py     # API client for server communication
    ├── ui/
    │   ├── styles.py     # UI styling and theming
    │   ├── components.py # Custom UI components
    │   └── task_form.py  # Task creation/editing dialog
    └── utils/
        └── connection_manager.py  # Connection monitoring
```

## Features Overview

### Connection Management
- Continuous monitoring of server connection
- App becomes unusable when disconnected
- Automatic reconnection attempts
- Real-time connection status indicator

### Task Management
- Create new tasks with title, description, priority, and due date
- Edit existing tasks
- Delete tasks with confirmation
- Toggle task completion and pause status
- Visual priority indicators (High: Red, Medium: Orange, Low: Green)

### Filtering System
- Filter by priority range (0-100)
- Show/hide completed tasks
- Show/hide incomplete tasks
- Show/hide paused tasks
- Real-time filter application

### Modern UI
- Clean, modern design with proper spacing
- Hover effects on interactive elements
- Color-coded priority system
- Responsive layout with scrolling
- Modal dialogs for task creation/editing

## API Endpoints Used

The app uses all available API endpoints:

- `GET /health` - Health check
- `GET /tasks` - Get all tasks
- `POST /tasks` - Create new task
- `GET /tasks/{id}` - Get specific task
- `PUT /tasks/{id}` - Update task
- `DELETE /tasks/{id}` - Delete task
- `GET /tasks/priority/{min}/{max}` - Filter by priority
- `GET /tasks/status/{completed}` - Filter by completion status
- `GET /tasks/paused/{paused}` - Filter by paused status

## Error Handling

- Network errors are handled gracefully
- User-friendly error messages
- Connection loss detection and recovery
- Form validation for task creation/editing

## Troubleshooting

1. **Connection Issues**: Ensure the API server is running on the configured URL
2. **Import Errors**: Run `pip install -r requirements.txt`
3. **UI Issues**: Ensure tkinter is available (usually comes with Python)
4. **Performance**: Large task lists are handled with scrolling and efficient updates