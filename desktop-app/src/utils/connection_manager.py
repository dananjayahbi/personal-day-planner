"""
Connection Manager for Personal Day Planner Desktop App
Ensures the app is always connected to the server
"""

import requests
import threading
import time
from typing import Callable, Optional
import sys
import os

# No longer need config imports since we use base_url directly


class ConnectionManager:
    """Manages connection to the API server and handles reconnection logic"""
    
    def __init__(self, base_url: str, connection_callback: Optional[Callable[[bool], None]] = None):
        """
        Initialize connection manager
        
        Args:
            base_url: Base URL of the API server
            connection_callback: Function to call when connection status changes
        """
        self.base_url = base_url
        self.is_connected = False
        self.connection_callback = connection_callback
        self.monitoring_thread = None
        self.should_monitor = False
        self.connection_timeout = 5  # seconds
        self.check_interval = 3  # seconds
        
    def check_connection(self) -> bool:
        """
        Check if server is reachable
        
        Returns:
            bool: True if connected, False otherwise
        """
        try:
            health_url = f"{self.base_url}/health"
            response = requests.get(
                health_url,
                timeout=self.connection_timeout
            )
            is_connected = response.status_code == 200
            self.is_connected = is_connected
            return is_connected
        except (requests.exceptions.RequestException, Exception):
            self.is_connected = False
            return False
    
    def start_monitoring(self):
        """Start continuous connection monitoring in background thread"""
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            return
        
        self.should_monitor = True
        self.monitoring_thread = threading.Thread(
            target=self._monitor_connection,
            daemon=True
        )
        self.monitoring_thread.start()
    
    def stop_monitoring(self):
        """Stop connection monitoring"""
        self.should_monitor = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=1)
    
    def _monitor_connection(self):
        """Internal method to continuously monitor connection"""
        while self.should_monitor:
            current_status = self.check_connection()
            
            # If status changed, notify callback
            if current_status != self.is_connected:
                self.is_connected = current_status
                if self.connection_callback:
                    try:
                        self.connection_callback(self.is_connected)
                    except Exception as e:
                        print(f"Error in connection callback: {e}")
            
            time.sleep(self.check_interval)
    
    def wait_for_connection(self, max_attempts: int = 10) -> bool:
        """
        Wait for connection to be established
        
        Args:
            max_attempts: Maximum number of attempts before giving up
            
        Returns:
            bool: True if connection established, False if failed
        """
        attempts = 0
        while attempts < max_attempts:
            if self.check_connection():
                self.is_connected = True
                return True
            
            attempts += 1
            time.sleep(2)
        
        return False
    
    def get_connection_status(self) -> bool:
        """Get current connection status"""
        return self.is_connected


class ConnectionRequiredError(Exception):
    """Raised when trying to use API while disconnected"""
    pass


def require_connection(func):
    """
    Decorator to ensure function only runs when connected
    
    Args:
        func: Function to wrap
        
    Returns:
        Wrapped function that checks connection first
    """
    def wrapper(*args, **kwargs):
        # Get connection manager from first argument (usually self)
        if hasattr(args[0], 'connection_manager'):
            if not args[0].connection_manager.get_connection_status():
                raise ConnectionRequiredError("No connection to server")
        return func(*args, **kwargs)
    return wrapper


# Global connection manager instance
_connection_manager = None

def get_connection_manager() -> ConnectionManager:
    """Get global connection manager instance"""
    global _connection_manager
    if _connection_manager is None:
        _connection_manager = ConnectionManager()
    return _connection_manager