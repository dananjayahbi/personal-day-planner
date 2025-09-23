"""
API Configuration for Personal Day Planner Desktop App
"""

class APIConfig:
    """Configuration class for API endpoints"""
    
    # Base URL - Change this when server is deployed to cloud
    BASE_URL = "http://localhost:8000"
    
    # API Endpoints
    ENDPOINTS = {
        # Health check endpoints
        "root": "/",
        "health": "/health",
        
        # Task management endpoints
        "tasks": "/tasks",
        "task_by_id": "/tasks/{task_id}",
        
        # Filter endpoints
        "tasks_by_priority": "/tasks/priority/{min_priority}/{max_priority}",
        "tasks_by_status": "/tasks/status/{completed}",
        "tasks_by_paused": "/tasks/paused/{paused}",
    }
    
    # Request timeouts (in seconds)
    TIMEOUTS = {
        "connection": 5,
        "read": 10,
        "total": 15
    }
    
    # Retry configuration
    RETRY_CONFIG = {
        "max_retries": 3,
        "backoff_factor": 0.5
    }
    
    @classmethod
    def get_url(cls, endpoint_key, **kwargs):
        """
        Get full URL for an endpoint with optional path parameters
        
        Args:
            endpoint_key (str): Key from ENDPOINTS dict
            **kwargs: Path parameters to format into the URL
            
        Returns:
            str: Full URL for the endpoint
        """
        endpoint = cls.ENDPOINTS.get(endpoint_key)
        if not endpoint:
            raise ValueError(f"Unknown endpoint: {endpoint_key}")
        
        # Format path parameters if provided
        if kwargs:
            endpoint = endpoint.format(**kwargs)
        
        return f"{cls.BASE_URL}{endpoint}"
    
    @classmethod
    def set_base_url(cls, new_base_url):
        """
        Update the base URL (useful for switching between dev and production)
        
        Args:
            new_base_url (str): New base URL without trailing slash
        """
        cls.BASE_URL = new_base_url.rstrip('/')


# Quick access functions for common URLs
def get_tasks_url():
    """Get URL for tasks endpoint"""
    return APIConfig.get_url("tasks")

def get_task_url(task_id):
    """Get URL for specific task"""
    return APIConfig.get_url("task_by_id", task_id=task_id)

def get_health_url():
    """Get URL for health check"""
    return APIConfig.get_url("health")

def get_priority_filter_url(min_priority, max_priority):
    """Get URL for priority filter"""
    return APIConfig.get_url("tasks_by_priority", 
                            min_priority=min_priority, 
                            max_priority=max_priority)

def get_status_filter_url(completed):
    """Get URL for completion status filter"""
    return APIConfig.get_url("tasks_by_status", completed=str(completed).lower())

def get_paused_filter_url(paused):
    """Get URL for paused status filter"""
    return APIConfig.get_url("tasks_by_paused", paused=str(paused).lower())

# Static configuration for easy access
API_CONFIG = {
    "base_url": APIConfig.BASE_URL,
    "endpoints": APIConfig.ENDPOINTS,
    "timeouts": APIConfig.TIMEOUTS,
    "retry": APIConfig.RETRY_CONFIG
}