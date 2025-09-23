"""
Main Application Window for Personal Day Planner Desktop App
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
import time
import sys
import os

# Add parent directories to path for imports
current_dir = os.path.dirname(__file__)
src_dir = os.path.dirname(current_dir)
app_dir = os.path.dirname(src_dir)
config_dir = os.path.join(app_dir, 'config')

sys.path.extend([current_dir, src_dir, app_dir, config_dir])

try:
    from ui.styles import *
    from ui.components import *
    from ui.task_form import TaskFormDialog
    from api.client import TaskAPIClient, APIError
    from utils.connection_manager import ConnectionManager, get_connection_manager
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure you're running from the correct directory")
    sys.exit(1)


class TaskManagerApp:
    """Main application class for Task Manager"""
    
    def __init__(self):
        """Initialize the application"""
        self.root = tk.Tk()
        self.root.title("Personal Day Planner")
        self.root.geometry(f"{Spacing.WINDOW_DEFAULT_WIDTH}x{Spacing.WINDOW_DEFAULT_HEIGHT}")
        self.root.minsize(Spacing.WINDOW_MIN_WIDTH, Spacing.WINDOW_MIN_HEIGHT)
        self.root.configure(bg=Colors.BG_PRIMARY)
        
        # Initialize connection manager and API client
        self.connection_manager = get_connection_manager()
        self.connection_manager.connection_callback = self._on_connection_change
        self.api_client = TaskAPIClient(self.connection_manager)
        
        # Application state
        self.tasks = []
        self.filtered_tasks = []
        self.current_filters = {}
        self.app_enabled = False
        
        self._create_widgets()
        self._setup_connection()
        
        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _create_widgets(self):
        """Create main application widgets"""
        # Main container
        main_container = tk.Frame(self.root, **Styles.FRAME_DEFAULT)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Connection status bar
        self.status_bar = ConnectionStatusBar(main_container)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Main content area
        content_frame = tk.Frame(main_container, **Styles.FRAME_DEFAULT)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Filters
        left_panel = tk.Frame(content_frame, **Styles.FRAME_SECONDARY, width=250)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 1))
        left_panel.pack_propagate(False)
        
        self.filter_panel = FilterPanel(left_panel, on_filter_change=self._on_filter_change)
        self.filter_panel.pack(fill=tk.BOTH, expand=True)
        
        # Right panel - Main content
        right_panel = tk.Frame(content_frame, **Styles.FRAME_DEFAULT)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = tk.Frame(right_panel, **Styles.FRAME_DEFAULT)
        header_frame.pack(fill=tk.X, padx=Spacing.PAD_LARGE, pady=(Spacing.PAD_LARGE, 0))
        
        title_label = tk.Label(header_frame, text="Task Manager", **Styles.LABEL_TITLE)
        title_label.pack(side=tk.LEFT)
        
        # Action buttons
        button_frame = tk.Frame(header_frame, **Styles.FRAME_DEFAULT)
        button_frame.pack(side=tk.RIGHT)
        
        self.refresh_btn = ModernButton(button_frame, text="🔄 Refresh", style_type="secondary",
                                      command=self._refresh_tasks)
        self.refresh_btn.pack(side=tk.LEFT, padx=(0, Spacing.PAD_SMALL))
        
        self.create_btn = ModernButton(button_frame, text="+ New Task", style_type="success",
                                     command=self._create_task)
        self.create_btn.pack(side=tk.LEFT)
        
        # Task counter
        counter_frame = tk.Frame(right_panel, **Styles.FRAME_DEFAULT)
        counter_frame.pack(fill=tk.X, padx=Spacing.PAD_LARGE, pady=(Spacing.PAD_SMALL, 0))
        
        self.task_counter = tk.Label(counter_frame, text="No tasks", **Styles.LABEL_SECONDARY)
        self.task_counter.pack(side=tk.LEFT)
        
        # Tasks container with scrollbar
        tasks_container = tk.Frame(right_panel, **Styles.FRAME_DEFAULT)
        tasks_container.pack(fill=tk.BOTH, expand=True, padx=Spacing.PAD_LARGE, 
                           pady=(Spacing.PAD_MEDIUM, Spacing.PAD_LARGE))
        
        # Create scrollable frame
        self.canvas = tk.Canvas(tasks_container, **Styles.FRAME_DEFAULT, highlightthickness=0)
        scrollbar = tk.Scrollbar(tasks_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, **Styles.FRAME_DEFAULT)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel to canvas
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        
        # Disabled overlay
        self.disabled_overlay = tk.Frame(self.root, bg=Colors.BG_SECONDARY)
        self.disabled_message = tk.Label(
            self.disabled_overlay,
            text="Connecting to server...\nPlease wait.",
            font=(Fonts.FAMILY_DEFAULT, Fonts.SIZE_LARGE, Fonts.WEIGHT_BOLD),
            fg=Colors.TEXT_SECONDARY,
            bg=Colors.BG_SECONDARY
        )
        self.disabled_message.pack(expand=True)
        
        # Initially disable the app
        self._disable_app("Connecting to server...")
    
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def _setup_connection(self):
        """Setup connection monitoring"""
        self.connection_manager.start_monitoring()
        
        # Try initial connection in background
        threading.Thread(target=self._initial_connection_check, daemon=True).start()
    
    def _initial_connection_check(self):
        """Check initial connection"""
        if self.connection_manager.wait_for_connection(max_attempts=5):
            self.root.after(0, lambda: self._on_connection_change(True))
        else:
            self.root.after(0, lambda: self._on_connection_change(False))
    
    def _on_connection_change(self, connected: bool):
        """Handle connection status change"""
        self.status_bar.update_status(connected)
        
        if connected:
            self._enable_app()
            self._refresh_tasks()
        else:
            self._disable_app("No connection to server")
    
    def _enable_app(self):
        """Enable application interface"""
        self.app_enabled = True
        self.disabled_overlay.pack_forget()
        
        # Enable buttons
        for widget in [self.refresh_btn, self.create_btn]:
            widget.configure(state="normal")
    
    def _disable_app(self, message: str):
        """Disable application interface"""
        self.app_enabled = False
        
        # Show overlay
        self.disabled_overlay.pack(fill=tk.BOTH, expand=True)
        self.disabled_message.config(text=message)
        
        # Disable buttons
        for widget in [self.refresh_btn, self.create_btn]:
            widget.configure(state="disabled")
    
    def _refresh_tasks(self):
        """Refresh task list from server"""
        if not self.app_enabled:
            return
        
        try:
            self.tasks = self.api_client.get_all_tasks()
            self._apply_filters()
            self._update_task_display()
        except APIError as e:
            messagebox.showerror("Error", f"Failed to load tasks: {e.message}")
    
    def _create_task(self):
        """Create new task"""
        if not self.app_enabled:
            return
        
        dialog = TaskFormDialog(self.root, title="Create New Task")
        result = dialog.show()
        
        if result:
            try:
                self.api_client.create_task(result)
                self._refresh_tasks()
                messagebox.showinfo("Success", "Task created successfully!")
            except APIError as e:
                messagebox.showerror("Error", f"Failed to create task: {e.message}")
    
    def _edit_task(self, task_data):
        """Edit existing task"""
        if not self.app_enabled:
            return
        
        dialog = TaskFormDialog(self.root, task_data=task_data, title="Edit Task")
        result = dialog.show()
        
        if result:
            try:
                self.api_client.update_task(task_data["id"], result)
                self._refresh_tasks()
                messagebox.showinfo("Success", "Task updated successfully!")
            except APIError as e:
                messagebox.showerror("Error", f"Failed to update task: {e.message}")
    
    def _delete_task(self, task_data):
        """Delete task"""
        if not self.app_enabled:
            return
        
        if messagebox.askyesno("Confirm Delete", 
                              f"Are you sure you want to delete '{task_data['title']}'?"):
            try:
                self.api_client.delete_task(task_data["id"])
                self._refresh_tasks()
                messagebox.showinfo("Success", "Task deleted successfully!")
            except APIError as e:
                messagebox.showerror("Error", f"Failed to delete task: {e.message}")
    
    def _toggle_task(self, task_data):
        """Toggle task completion/pause status"""
        if not self.app_enabled:
            return
        
        try:
            # Determine new status
            if task_data.get("completed"):
                # Mark as incomplete
                update_data = {"completed": False, "paused": False}
                message = "Task marked as incomplete"
            elif task_data.get("paused"):
                # Resume task
                update_data = {"paused": False}
                message = "Task resumed"
            else:
                # Complete task
                update_data = {"completed": True, "paused": False}
                message = "Task completed"
            
            self.api_client.update_task(task_data["id"], update_data)
            self._refresh_tasks()
            messagebox.showinfo("Success", message)
        except APIError as e:
            messagebox.showerror("Error", f"Failed to update task: {e.message}")
    
    def _on_filter_change(self, filters):
        """Handle filter changes"""
        self.current_filters = filters
        self._apply_filters()
        self._update_task_display()
    
    def _apply_filters(self):
        """Apply current filters to task list"""
        if not self.current_filters:
            self.filtered_tasks = self.tasks.copy()
            return
        
        filtered = []
        for task in self.tasks:
            # Priority filter
            priority = task.get("priority", 0)
            if not (self.current_filters["min_priority"] <= priority <= self.current_filters["max_priority"]):
                continue
            
            # Status filters
            completed = task.get("completed", False)
            paused = task.get("paused", False)
            
            if completed and not self.current_filters["show_completed"]:
                continue
            if not completed and not paused and not self.current_filters["show_incomplete"]:
                continue
            if paused and not self.current_filters["show_paused"]:
                continue
            
            filtered.append(task)
        
        self.filtered_tasks = filtered
    
    def _update_task_display(self):
        """Update task display"""
        # Clear existing task cards
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Update counter
        total_tasks = len(self.tasks)
        filtered_count = len(self.filtered_tasks)
        
        if total_tasks == 0:
            self.task_counter.config(text="No tasks")
        elif filtered_count == total_tasks:
            self.task_counter.config(text=f"{total_tasks} tasks")
        else:
            self.task_counter.config(text=f"{filtered_count} of {total_tasks} tasks")
        
        # Create task cards
        if not self.filtered_tasks:
            no_tasks_label = tk.Label(
                self.scrollable_frame,
                text="No tasks to display" if self.tasks else "Create your first task!",
                **Styles.LABEL_SECONDARY
            )
            no_tasks_label.pack(pady=Spacing.PAD_LARGE)
        else:
            # Sort tasks by priority (high to low) and creation date
            sorted_tasks = sorted(
                self.filtered_tasks,
                key=lambda x: (-x.get("priority", 0), x.get("created_at", ""))
            )
            
            for task in sorted_tasks:
                card = TaskCard(
                    self.scrollable_frame,
                    task,
                    on_edit=self._edit_task,
                    on_delete=self._delete_task,
                    on_toggle=self._toggle_task
                )
                card.pack(fill=tk.X, pady=(0, Spacing.PAD_SMALL))
    
    def _on_closing(self):
        """Handle application closing"""
        self.connection_manager.stop_monitoring()
        self.root.quit()
        self.root.destroy()
    
    def run(self):
        """Run the application"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self._on_closing()


def main():
    """Main entry point"""
    app = TaskManagerApp()
    app.run()


if __name__ == "__main__":
    main()