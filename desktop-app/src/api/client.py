"""
API Client for Personal Day Planner Desktop App
Handles all API communications with the server
"""

import requests
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
import sys
import os

# Add config directory to path for imports
config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config')
sys.path.append(config_path)
utils_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'utils')
sys.path.append(utils_path)

try:
    from api_config import *
except ImportError:
    # Fallback API configuration
    def get_health_url():
        return "http://localhost:8000/health"
    def get_tasks_url():
        return "http://localhost:8000/tasks"
    def get_task_url(task_id):
        return f"http://localhost:8000/tasks/{task_id}"
    def get_priority_filter_url(min_priority, max_priority):
        return f"http://localhost:8000/tasks/priority/{min_priority}/{max_priority}"
    def get_status_filter_url(completed):
        return f"http://localhost:8000/tasks/status/{str(completed).lower()}"
    def get_paused_filter_url(paused):
        return f"http://localhost:8000/tasks/paused/{str(paused).lower()}"

try:
    from connection_manager import require_connection, ConnectionRequiredError
except ImportError:
    # Fallback decorators
    def require_connection(func):
        return func
    class ConnectionRequiredError(Exception):
        pass


class TaskAPIClient:
    """Client for interacting with the Task Management API"""
    
    def __init__(self, connection_manager):
        """
        Initialize API client
        
        Args:
            connection_manager: ConnectionManager instance
        """
        self.connection_manager = connection_manager
        self.base_url = connection_manager.base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    @require_connection
    def get_health(self) -> Dict[str, Any]:
        """
        Get server health status
        
        Returns:
            Dict containing health information
        """
        url = f"{self.base_url}/health"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    @require_connection
    def create_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new task
        
        Args:
            task_data: Task information (title, description, priority, etc.)
            
        Returns:
            Dict containing created task information
        """
        url = f"{self.base_url}/tasks"
        response = self.session.post(url, json=task_data)
        response.raise_for_status()
        return response.json()
    
    @require_connection
    def get_all_tasks(self) -> List[Dict[str, Any]]:
        """
        Get all tasks
        
        Returns:
            List of task dictionaries
        """
        url = f"{self.base_url}/tasks"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    @require_connection
    def get_task(self, task_id: str) -> Dict[str, Any]:
        """
        Get a specific task by ID
        
        Args:
            task_id: Task ID
            
        Returns:
            Dict containing task information
        """
        url = f"{self.base_url}/tasks/{task_id}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    @require_connection
    def update_task(self, task_id: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing task
        
        Args:
            task_id: Task ID
            task_data: Updated task information
            
        Returns:
            Dict containing updated task information
        """
        url = f"{self.base_url}/tasks/{task_id}"
        response = self.session.put(url, json=task_data)
        response.raise_for_status()
        return response.json()
    
    @require_connection
    def delete_task(self, task_id: str) -> bool:
        """
        Delete a task
        
        Args:
            task_id: Task ID
            
        Returns:
            True if successful
        """
        url = f"{self.base_url}/tasks/{task_id}"
        response = self.session.delete(url)
        response.raise_for_status()
        return True
    
    @require_connection
    def get_tasks_by_priority(self, min_priority: float, max_priority: float) -> List[Dict[str, Any]]:
        """
        Get tasks within priority range
        
        Args:
            min_priority: Minimum priority (0-100)
            max_priority: Maximum priority (0-100)
            
        Returns:
            List of task dictionaries
        """
        url = f"{self.base_url}/tasks/priority/{min_priority}/{max_priority}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    @require_connection
    def get_tasks_by_status(self, completed: bool) -> List[Dict[str, Any]]:
        """
        Get tasks by completion status
        
        Args:
            completed: True for completed tasks, False for incomplete
            
        Returns:
            List of task dictionaries
        """
        url = f"{self.base_url}/tasks/status/{str(completed).lower()}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    @require_connection
    def get_tasks_by_paused_status(self, paused: bool) -> List[Dict[str, Any]]:
        """
        Get tasks by paused status
        
        Args:
            paused: True for paused tasks, False for active
            
        Returns:
            List of task dictionaries
        """
        url = f"{self.base_url}/tasks/paused/{str(paused).lower()}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()


class APIError(Exception):
    """Custom exception for API errors"""
    
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


def handle_api_error(func):
    """
    Decorator to handle API errors gracefully
    
    Args:
        func: Function to wrap
        
    Returns:
        Wrapped function with error handling
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ConnectionRequiredError:
            raise APIError("No connection to server")
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if e.response else None
            try:
                error_detail = e.response.json().get('detail', str(e))
            except (ValueError, AttributeError):
                error_detail = str(e)
            raise APIError(f"HTTP Error: {error_detail}", status_code)
        except requests.exceptions.RequestException as e:
            raise APIError(f"Request Error: {str(e)}")
        except Exception as e:
            raise APIError(f"Unexpected Error: {str(e)}")
    
    return wrapper


# Apply error handling to all API client methods
for method_name in dir(TaskAPIClient):
    if not method_name.startswith('_') and callable(getattr(TaskAPIClient, method_name)):
        method = getattr(TaskAPIClient, method_name)
        if method_name != '__init__':
            setattr(TaskAPIClient, method_name, handle_api_error(method))