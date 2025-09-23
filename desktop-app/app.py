import tkinter as tk
from tkinter import messagebox
import sys
import os
import asyncio
import threading
from datetime import datetime

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.api.client import TaskAPIClient
from src.utils.connection_manager import ConnectionManager
from src.ui.modern_styles import ModernStyles
from src.ui.task_list import ModernTaskList
from src.ui.task_form import TaskForm
from config.api_config import API_CONFIG

class ModernTaskManager:
    def __init__(self):
        self.root = None
        self.connection_manager = None
        self.api_client = None
        self.task_list = None
        self.tasks = []
        self.connection_status_label = None
        
    def initialize(self):
        """Initialize the application"""
        self.setup_window()
        self.setup_connection()
        self.setup_ui()
        self.check_connection()
        
    def setup_window(self):
        """Setup main window"""
        self.root = tk.Tk()
        self.root.title("Personal Day Planner - Task Manager")
        self.root.geometry("900x700")
        self.root.minsize(ModernStyles.DIMENSIONS['window_min_width'], 
                         ModernStyles.DIMENSIONS['window_min_height'])
        self.root.configure(bg=ModernStyles.COLORS['bg_primary'])
        
        # Center window
        self.center_window()
        
        # Set window icon and properties
        try:
            self.root.iconbitmap(default='')  # Remove default icon
        except:
            pass
            
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def setup_connection(self):
        """Setup API connection"""
        self.connection_manager = ConnectionManager(API_CONFIG['base_url'])
        self.api_client = TaskAPIClient(self.connection_manager)
        
    def setup_ui(self):
        """Setup user interface"""
        # Main container
        main_container = tk.Frame(self.root, **ModernStyles.get_frame_style('primary'))
        main_container.pack(fill='both', expand=True)
        
        # Header section
        self.create_header(main_container)
        
        # Toolbar section
        self.create_toolbar(main_container)
        
        # Task list section
        self.create_task_section(main_container)
        
        # Status bar
        self.create_status_bar(main_container)
        
    def create_header(self, parent):
        """Create application header"""
        header_frame = tk.Frame(parent, **ModernStyles.get_frame_style('secondary'))
        header_frame.pack(fill='x', padx=ModernStyles.SPACING['medium'], 
                         pady=(ModernStyles.SPACING['medium'], 0))
        
        # App title and description
        title_container = tk.Frame(header_frame, **ModernStyles.get_frame_style('secondary'))
        title_container.pack(side='left', fill='y', pady=ModernStyles.SPACING['medium'])
        
        app_title = tk.Label(title_container, text="Personal Day Planner", 
                            **ModernStyles.get_label_style('title'))
        app_title.pack(anchor='w')
        
        app_subtitle = tk.Label(title_container, text="Task Management Interface", 
                               **ModernStyles.get_label_style('small'))
        app_subtitle.pack(anchor='w')
        
        # Connection status
        status_container = tk.Frame(header_frame, **ModernStyles.get_frame_style('secondary'))
        status_container.pack(side='right', fill='y', pady=ModernStyles.SPACING['medium'])
        
        self.connection_status_label = tk.Label(status_container, text="● Checking connection...", 
                                               **ModernStyles.get_label_style('body'))
        self.connection_status_label.pack(anchor='e')
        
    def create_toolbar(self, parent):
        """Create toolbar with action buttons"""
        toolbar_frame = tk.Frame(parent, **ModernStyles.get_frame_style('tertiary'))
        toolbar_frame.pack(fill='x', padx=ModernStyles.SPACING['medium'], 
                          pady=ModernStyles.SPACING['small'])
        
        # Action buttons
        buttons_data = [
            ('+ New Task', 'primary', self.create_new_task),
            ('↻ Refresh', 'secondary', self.refresh_tasks),
        ]
        
        for text, style, command in buttons_data:
            btn = tk.Button(toolbar_frame, text=text, command=command,
                           **ModernStyles.get_button_style(style))
            btn.pack(side='left', padx=(0, ModernStyles.SPACING['small']),
                    ipadx=ModernStyles.SPACING['medium'])
        
        # Filter section on the right
        filter_frame = tk.Frame(toolbar_frame, **ModernStyles.get_frame_style('tertiary'))
        filter_frame.pack(side='right')
        
        tk.Label(filter_frame, text="Filter:", **ModernStyles.get_label_style('body')).pack(side='left')
        
        filter_buttons = [
            ('All', self.show_all_tasks),
            ('Active', self.show_active_tasks),
            ('Completed', self.show_completed_tasks),
        ]
        
        for text, command in filter_buttons:
            btn = tk.Button(filter_frame, text=text, command=command,
                           **ModernStyles.get_button_style('secondary'))
            btn.pack(side='left', padx=(ModernStyles.SPACING['small'], 0),
                    ipadx=ModernStyles.SPACING['small'])
        
    def create_task_section(self, parent):
        """Create task list section"""
        task_container = tk.Frame(parent, **ModernStyles.get_frame_style('primary'))
        task_container.pack(fill='both', expand=True, padx=ModernStyles.SPACING['medium'],
                           pady=ModernStyles.SPACING['small'])
        
        # Create modern task list
        self.task_list = ModernTaskList(
            task_container,
            on_task_select=self.edit_task,
            on_task_update=self.handle_task_update
        )
        
    def create_status_bar(self, parent):
        """Create status bar"""
        status_frame = tk.Frame(parent, **ModernStyles.get_frame_style('tertiary'))
        status_frame.pack(fill='x', padx=ModernStyles.SPACING['medium'],
                         pady=(0, ModernStyles.SPACING['medium']))
        
        # Status info
        self.status_label = tk.Label(status_frame, text="Ready", 
                                    **ModernStyles.get_label_style('small'))
        self.status_label.pack(side='left', padx=ModernStyles.SPACING['medium'],
                              pady=ModernStyles.SPACING['small'])
        
        # Server info
        server_info = tk.Label(status_frame, text=f"Server: {API_CONFIG['base_url']}", 
                              **ModernStyles.get_label_style('small'))
        server_info.pack(side='right', padx=ModernStyles.SPACING['medium'],
                        pady=ModernStyles.SPACING['small'])
        
    def check_connection(self):
        """Check server connection"""
        def check():
            try:
                is_connected = self.connection_manager.check_connection()
                self.root.after(0, self.update_connection_status, is_connected)
                
                if is_connected:
                    self.root.after(0, self.load_tasks)
                else:
                    self.root.after(0, self.show_connection_error)
                    
            except Exception as e:
                self.root.after(0, self.update_connection_status, False, str(e))
        
        # Run connection check in background thread
        threading.Thread(target=check, daemon=True).start()
        
    def update_connection_status(self, is_connected, error_msg=None):
        """Update connection status display"""
        if is_connected:
            self.connection_status_label.config(
                text="● Connected",
                **ModernStyles.get_label_style('success')
            )
            self.status_label.config(text="Connected to server")
        else:
            self.connection_status_label.config(
                text="● Disconnected",
                **ModernStyles.get_label_style('error')
            )
            error_text = f"Connection failed: {error_msg}" if error_msg else "Server unavailable"
            self.status_label.config(text=error_text)
            
    def show_connection_error(self):
        """Show connection error dialog"""
        result = messagebox.askretrycancel(
            "Connection Error",
            "Cannot connect to the server. Please make sure the server is running.\n\n"
            f"Server URL: {API_CONFIG['base_url']}\n\n"
            "Would you like to retry?",
            icon="error"
        )
        
        if result:
            self.check_connection()
        else:
            self.root.quit()
            
    def load_tasks(self):
        """Load tasks from server"""
        def load():
            try:
                tasks = self.api_client.get_all_tasks()
                self.root.after(0, self.update_task_display, tasks)
            except Exception as e:
                self.root.after(0, self.show_error, f"Failed to load tasks: {str(e)}")
        
        threading.Thread(target=load, daemon=True).start()
        self.status_label.config(text="Loading tasks...")
        
    def update_task_display(self, tasks):
        """Update task display"""
        self.tasks = tasks
        self.task_list.update_tasks(tasks)
        self.status_label.config(text=f"Loaded {len(tasks)} tasks")
        
    def create_new_task(self):
        """Create new task"""
        if not self.connection_manager.check_connection():
            self.show_error("Cannot create task: No server connection")
            return
            
        form = TaskForm(self.root, on_save=self.save_new_task)
        form.show()
        
    def edit_task(self, task):
        """Edit existing task"""
        if not self.connection_manager.check_connection():
            self.show_error("Cannot edit task: No server connection")
            return
            
        form = TaskForm(self.root, on_save=self.save_edited_task, task_data=task)
        form.show()
        
    def save_new_task(self, task_data):
        """Save new task"""
        def save():
            try:
                created_task = self.api_client.create_task(task_data)
                self.root.after(0, self.on_task_saved, created_task)
            except Exception as e:
                self.root.after(0, self.show_error, f"Failed to create task: {str(e)}")
        
        threading.Thread(target=save, daemon=True).start()
        self.status_label.config(text="Creating task...")
        
    def save_edited_task(self, task_data):
        """Save edited task"""
        def save():
            try:
                task_id = task_data.pop('id')
                updated_task = self.api_client.update_task(task_id, task_data)
                self.root.after(0, self.on_task_saved, updated_task)
            except Exception as e:
                self.root.after(0, self.show_error, f"Failed to update task: {str(e)}")
        
        threading.Thread(target=save, daemon=True).start()
        self.status_label.config(text="Updating task...")
        
    def on_task_saved(self, task):
        """Handle task save completion"""
        self.load_tasks()  # Refresh the list
        self.status_label.config(text="Task saved successfully")
        
    def handle_task_update(self, action, task):
        """Handle quick task updates"""
        if action == 'refresh':
            self.refresh_tasks()
        elif action == 'complete' and task:
            self.quick_update_task(task, {'completed': True})
        elif action == 'pause' and task:
            current_paused = task.get('paused', False)
            self.quick_update_task(task, {'paused': not current_paused})
        elif action == 'delete' and task:
            self.delete_task(task)
            
    def quick_update_task(self, task, updates):
        """Quick update task status"""
        def update():
            try:
                updated_task = self.api_client.update_task(task['id'], updates)
                self.root.after(0, self.on_task_saved, updated_task)
            except Exception as e:
                self.root.after(0, self.show_error, f"Failed to update task: {str(e)}")
        
        threading.Thread(target=update, daemon=True).start()
        self.status_label.config(text="Updating task...")
        
    def delete_task(self, task):
        """Delete a task"""
        result = messagebox.askyesno(
            "Delete Task",
            f"Are you sure you want to delete:\n'{task.get('title', 'Untitled')}'?",
            icon="warning"
        )
        
        if result:
            def delete():
                try:
                    self.api_client.delete_task(task['id'])
                    self.root.after(0, self.on_task_deleted)
                except Exception as e:
                    self.root.after(0, self.show_error, f"Failed to delete task: {str(e)}")
            
            threading.Thread(target=delete, daemon=True).start()
            self.status_label.config(text="Deleting task...")
            
    def on_task_deleted(self):
        """Handle task deletion completion"""
        self.load_tasks()  # Refresh the list
        self.status_label.config(text="Task deleted successfully")
        
    def refresh_tasks(self):
        """Refresh task list"""
        self.load_tasks()
        
    def show_all_tasks(self):
        """Show all tasks"""
        self.task_list.update_tasks(self.tasks)
        
    def show_active_tasks(self):
        """Show only active tasks"""
        active_tasks = [t for t in self.tasks if not t.get('completed', False)]
        self.task_list.update_tasks(active_tasks)
        
    def show_completed_tasks(self):
        """Show only completed tasks"""
        completed_tasks = [t for t in self.tasks if t.get('completed', False)]
        self.task_list.update_tasks(completed_tasks)
        
    def show_error(self, message):
        """Show error message"""
        messagebox.showerror("Error", message)
        self.status_label.config(text="Error occurred")
        
    def run(self):
        """Run the application"""
        try:
            self.initialize()
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\nApplication interrupted by user")
        except Exception as e:
            print(f"Application error: {e}")
            messagebox.showerror("Application Error", f"An error occurred: {e}")

def main():
    """Main entry point"""
    app = ModernTaskManager()
    app.run()

if __name__ == "__main__":
    main()