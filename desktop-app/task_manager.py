"""
Personal Day Planner Desktop Application

A modern task management desktop application built with tkinter.
Connects to the Personal Day Planner API server for task management.
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext
import requests
import threading
import time
from datetime import datetime, timedelta
import json
import sys
import os

# ==============================================================================
# CONFIGURATION
# ==============================================================================

BASE_URL = "http://localhost:8000"

# API Endpoints
def get_health_url():
    return f"{BASE_URL}/health"

def get_tasks_url():
    return f"{BASE_URL}/tasks"

def get_task_url(task_id):
    return f"{BASE_URL}/tasks/{task_id}"

def get_priority_filter_url(min_priority, max_priority):
    return f"{BASE_URL}/tasks/priority/{min_priority}/{max_priority}"

def get_status_filter_url(completed):
    return f"{BASE_URL}/tasks/status/{str(completed).lower()}"

def get_paused_filter_url(paused):
    return f"{BASE_URL}/tasks/paused/{str(paused).lower()}"

# ==============================================================================
# STYLES AND COLORS
# ==============================================================================

class Colors:
    PRIMARY = "#2563eb"
    PRIMARY_DARK = "#1d4ed8"
    SECONDARY = "#64748b"
    SECONDARY_DARK = "#475569"
    BG_PRIMARY = "#ffffff"
    BG_SECONDARY = "#f8fafc"
    SUCCESS = "#22c55e"
    WARNING = "#f59e0b"
    ERROR = "#ef4444"
    TEXT_PRIMARY = "#1e293b"
    TEXT_SECONDARY = "#64748b"
    TEXT_LIGHT = "#94a3b8"
    TEXT_WHITE = "#ffffff"
    PRIORITY_HIGH = "#ef4444"
    PRIORITY_MEDIUM = "#f59e0b"
    PRIORITY_LOW = "#22c55e"
    CONNECTED = "#22c55e"
    DISCONNECTED = "#ef4444"

class Fonts:
    FAMILY_DEFAULT = "Segoe UI"
    SIZE_LARGE = 16
    SIZE_MEDIUM = 12
    SIZE_SMALL = 10
    SIZE_TITLE = 20
    SIZE_HEADER = 14

def get_priority_color(priority: float) -> str:
    if priority >= 75:
        return Colors.PRIORITY_HIGH
    elif priority >= 50:
        return Colors.PRIORITY_MEDIUM
    else:
        return Colors.PRIORITY_LOW

# ==============================================================================
# CONNECTION MANAGER
# ==============================================================================

class ConnectionManager:
    def __init__(self, connection_callback=None):
        self.is_connected = False
        self.connection_callback = connection_callback
        self.monitoring_thread = None
        self.should_monitor = False
        self.connection_timeout = 5
        self.check_interval = 3
    
    def check_connection(self) -> bool:
        try:
            response = requests.get(get_health_url(), timeout=self.connection_timeout)
            return response.status_code == 200
        except:
            return False
    
    def start_monitoring(self):
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            return
        self.should_monitor = True
        self.monitoring_thread = threading.Thread(target=self._monitor_connection, daemon=True)
        self.monitoring_thread.start()
    
    def stop_monitoring(self):
        self.should_monitor = False
    
    def _monitor_connection(self):
        while self.should_monitor:
            current_status = self.check_connection()
            if current_status != self.is_connected:
                self.is_connected = current_status
                if self.connection_callback:
                    try:
                        self.connection_callback(self.is_connected)
                    except:
                        pass
            time.sleep(self.check_interval)
    
    def wait_for_connection(self, max_attempts: int = 10) -> bool:
        attempts = 0
        while attempts < max_attempts:
            if self.check_connection():
                self.is_connected = True
                return True
            attempts += 1
            time.sleep(2)
        return False

# ==============================================================================
# API CLIENT
# ==============================================================================

class TaskAPIClient:
    def __init__(self, connection_manager):
        self.connection_manager = connection_manager
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def _check_connection(self):
        if not self.connection_manager.is_connected:
            raise Exception("No connection to server")
    
    def get_health(self):
        self._check_connection()
        response = self.session.get(get_health_url())
        response.raise_for_status()
        return response.json()
    
    def create_task(self, task_data):
        self._check_connection()
        response = self.session.post(get_tasks_url(), json=task_data)
        response.raise_for_status()
        return response.json()
    
    def get_all_tasks(self):
        self._check_connection()
        response = self.session.get(get_tasks_url())
        response.raise_for_status()
        return response.json()
    
    def get_task(self, task_id):
        self._check_connection()
        response = self.session.get(get_task_url(task_id))
        response.raise_for_status()
        return response.json()
    
    def update_task(self, task_id, task_data):
        self._check_connection()
        response = self.session.put(get_task_url(task_id), json=task_data)
        response.raise_for_status()
        return response.json()
    
    def delete_task(self, task_id):
        self._check_connection()
        response = self.session.delete(get_task_url(task_id))
        response.raise_for_status()
        return True

# ==============================================================================
# UI COMPONENTS
# ==============================================================================

class ModernButton(tk.Button):
    def __init__(self, parent, style_type="primary", **kwargs):
        styles = {
            "primary": {"bg": Colors.PRIMARY, "fg": Colors.TEXT_WHITE},
            "secondary": {"bg": Colors.SECONDARY, "fg": Colors.TEXT_WHITE},
            "success": {"bg": Colors.SUCCESS, "fg": Colors.TEXT_WHITE},
            "danger": {"bg": Colors.ERROR, "fg": Colors.TEXT_WHITE}
        }
        
        style = styles.get(style_type, styles["primary"])
        config = {
            "font": (Fonts.FAMILY_DEFAULT, Fonts.SIZE_MEDIUM, "bold"),
            "relief": "flat",
            "borderwidth": 0,
            "padx": 10,
            "pady": 5,
            "cursor": "hand2",
            **style,
            **kwargs
        }
        super().__init__(parent, **config)

class TaskCard(tk.Frame):
    def __init__(self, parent, task_data, on_edit=None, on_delete=None, on_toggle=None, **kwargs):
        super().__init__(parent, bg=Colors.BG_PRIMARY, relief="solid", borderwidth=1, **kwargs)
        self.task_data = task_data
        self.on_edit = on_edit
        self.on_delete = on_delete
        self.on_toggle = on_toggle
        self._create_widgets()
    
    def _create_widgets(self):
        main_frame = tk.Frame(self, bg=Colors.BG_PRIMARY)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header_frame = tk.Frame(main_frame, bg=Colors.BG_PRIMARY)
        header_frame.pack(fill=tk.X, pady=(0, 5))
        
        title_label = tk.Label(header_frame, text=self.task_data.get("title", ""),
                              font=(Fonts.FAMILY_DEFAULT, Fonts.SIZE_HEADER, "bold"),
                              fg=Colors.TEXT_PRIMARY, bg=Colors.BG_PRIMARY)
        title_label.pack(side=tk.LEFT)
        
        # Priority indicator
        priority = self.task_data.get("priority", 0)
        priority_color = get_priority_color(priority)
        priority_frame = tk.Frame(header_frame, bg=priority_color, width=30, height=20)
        priority_frame.pack(side=tk.RIGHT, padx=(5, 0))
        priority_frame.pack_propagate(False)
        
        priority_label = tk.Label(priority_frame, text=f"{int(priority)}",
                                fg=Colors.TEXT_WHITE, bg=priority_color,
                                font=(Fonts.FAMILY_DEFAULT, Fonts.SIZE_SMALL, "bold"))
        priority_label.pack(expand=True)
        
        # Description
        description = self.task_data.get("description", "")
        if description:
            if len(description) > 100:
                description = description[:100] + "..."
            desc_label = tk.Label(main_frame, text=description,
                                font=(Fonts.FAMILY_DEFAULT, Fonts.SIZE_MEDIUM),
                                fg=Colors.TEXT_PRIMARY, bg=Colors.BG_PRIMARY)
            desc_label.pack(fill=tk.X, pady=(0, 5))
        
        # Status
        status_frame = tk.Frame(main_frame, bg=Colors.BG_PRIMARY)
        status_frame.pack(fill=tk.X, pady=(0, 5))
        
        completed = self.task_data.get("completed", False)
        paused = self.task_data.get("paused", False)
        
        if completed:
            status_text = "✓ Completed"
            status_color = Colors.SUCCESS
        elif paused:
            status_text = "⏸ Paused"
            status_color = Colors.WARNING
        else:
            status_text = "⏵ Active"
            status_color = Colors.PRIMARY
        
        status_label = tk.Label(status_frame, text=status_text,
                              font=(Fonts.FAMILY_DEFAULT, Fonts.SIZE_SMALL),
                              fg=status_color, bg=Colors.BG_PRIMARY)
        status_label.pack(side=tk.LEFT)
        
        # Due date
        due_date = self.task_data.get("due_date")
        if due_date:
            try:
                due_dt = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
                due_str = due_dt.strftime("%m/%d/%Y %H:%M")
                due_label = tk.Label(status_frame, text=f"Due: {due_str}",
                                   font=(Fonts.FAMILY_DEFAULT, Fonts.SIZE_SMALL),
                                   fg=Colors.TEXT_SECONDARY, bg=Colors.BG_PRIMARY)
                due_label.pack(side=tk.RIGHT)
            except:
                pass
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg=Colors.BG_PRIMARY)
        button_frame.pack(fill=tk.X, pady=(5, 0))
        
        if self.on_edit:
            edit_btn = ModernButton(button_frame, text="Edit", style_type="secondary",
                                  command=lambda: self.on_edit(self.task_data))
            edit_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        if self.on_delete:
            delete_btn = ModernButton(button_frame, text="Delete", style_type="danger",
                                    command=lambda: self.on_delete(self.task_data))
            delete_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        if self.on_toggle:
            if completed:
                toggle_text = "Mark Incomplete"
                toggle_style = "secondary"
            elif paused:
                toggle_text = "Resume"
                toggle_style = "success"
            else:
                toggle_text = "Complete"
                toggle_style = "success"
            
            toggle_btn = ModernButton(button_frame, text=toggle_text, style_type=toggle_style,
                                    command=lambda: self.on_toggle(self.task_data))
            toggle_btn.pack(side=tk.RIGHT)

# ==============================================================================
# TASK FORM DIALOG
# ==============================================================================

class TaskFormDialog:
    def __init__(self, parent, task_data=None, title="Create Task"):
        self.parent = parent
        self.task_data = task_data or {}
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x500")
        self.dialog.configure(bg=Colors.BG_PRIMARY)
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self._center_dialog()
        self._create_widgets()
    
    def _center_dialog(self):
        self.dialog.update_idletasks()
        x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - (400 // 2)
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - (500 // 2)
        self.dialog.geometry(f"400x500+{x}+{y}")
    
    def _create_widgets(self):
        main_frame = tk.Frame(self.dialog, bg=Colors.BG_PRIMARY)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="Task Details",
                              font=(Fonts.FAMILY_DEFAULT, Fonts.SIZE_TITLE, "bold"),
                              fg=Colors.TEXT_PRIMARY, bg=Colors.BG_PRIMARY)
        title_label.pack(pady=(0, 20))
        
        # Task Title
        tk.Label(main_frame, text="Title *",
                font=(Fonts.FAMILY_DEFAULT, Fonts.SIZE_HEADER, "bold"),
                fg=Colors.TEXT_PRIMARY, bg=Colors.BG_PRIMARY).pack(anchor=tk.W)
        
        self.title_entry = tk.Entry(main_frame, font=(Fonts.FAMILY_DEFAULT, Fonts.SIZE_MEDIUM))
        self.title_entry.pack(fill=tk.X, pady=(5, 15))
        
        if self.task_data.get("title"):
            self.title_entry.insert(0, self.task_data["title"])
        
        # Description
        tk.Label(main_frame, text="Description",
                font=(Fonts.FAMILY_DEFAULT, Fonts.SIZE_HEADER, "bold"),
                fg=Colors.TEXT_PRIMARY, bg=Colors.BG_PRIMARY).pack(anchor=tk.W)
        
        self.description_text = tk.Text(main_frame, height=6,
                                       font=(Fonts.FAMILY_DEFAULT, Fonts.SIZE_MEDIUM))
        self.description_text.pack(fill=tk.X, pady=(5, 15))
        
        if self.task_data.get("description"):
            self.description_text.insert(1.0, self.task_data["description"])
        
        # Priority
        tk.Label(main_frame, text="Priority",
                font=(Fonts.FAMILY_DEFAULT, Fonts.SIZE_HEADER, "bold"),
                fg=Colors.TEXT_PRIMARY, bg=Colors.BG_PRIMARY).pack(anchor=tk.W)
        
        self.priority_var = tk.DoubleVar(value=self.task_data.get("priority", 50.0))
        self.priority_scale = tk.Scale(main_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                                     variable=self.priority_var)
        self.priority_scale.pack(fill=tk.X, pady=(5, 15))
        
        # Due Date
        date_frame = tk.Frame(main_frame, bg=Colors.BG_PRIMARY)
        date_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(date_frame, text="Due Date (Optional)",
                font=(Fonts.FAMILY_DEFAULT, Fonts.SIZE_HEADER, "bold"),
                fg=Colors.TEXT_PRIMARY, bg=Colors.BG_PRIMARY).pack(anchor=tk.W)
        
        date_input_frame = tk.Frame(date_frame, bg=Colors.BG_PRIMARY)
        date_input_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.date_entry = tk.Entry(date_input_frame, width=15,
                                  font=(Fonts.FAMILY_DEFAULT, Fonts.SIZE_MEDIUM))
        self.date_entry.pack(side=tk.LEFT, padx=(0, 5))
        self.date_entry.insert(0, "YYYY-MM-DD")
        
        self.time_entry = tk.Entry(date_input_frame, width=10,
                                  font=(Fonts.FAMILY_DEFAULT, Fonts.SIZE_MEDIUM))
        self.time_entry.pack(side=tk.LEFT, padx=(0, 5))
        self.time_entry.insert(0, "HH:MM")
        
        today_btn = ModernButton(date_input_frame, text="Today", style_type="secondary",
                               command=self._set_today)
        today_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Set existing due date
        if self.task_data.get("due_date"):
            try:
                due_dt = datetime.fromisoformat(self.task_data["due_date"].replace('Z', '+00:00'))
                self.date_entry.delete(0, tk.END)
                self.date_entry.insert(0, due_dt.strftime("%Y-%m-%d"))
                self.time_entry.delete(0, tk.END)
                self.time_entry.insert(0, due_dt.strftime("%H:%M"))
            except:
                pass
        
        # Status checkboxes
        status_frame = tk.Frame(main_frame, bg=Colors.BG_PRIMARY)
        status_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(status_frame, text="Status",
                font=(Fonts.FAMILY_DEFAULT, Fonts.SIZE_HEADER, "bold"),
                fg=Colors.TEXT_PRIMARY, bg=Colors.BG_PRIMARY).pack(anchor=tk.W)
        
        checkbox_frame = tk.Frame(status_frame, bg=Colors.BG_PRIMARY)
        checkbox_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.completed_var = tk.BooleanVar(value=self.task_data.get("completed", False))
        completed_cb = tk.Checkbutton(checkbox_frame, text="Completed", variable=self.completed_var,
                                    bg=Colors.BG_PRIMARY)
        completed_cb.pack(side=tk.LEFT, padx=(0, 15))
        
        self.paused_var = tk.BooleanVar(value=self.task_data.get("paused", False))
        paused_cb = tk.Checkbutton(checkbox_frame, text="Paused", variable=self.paused_var,
                                 bg=Colors.BG_PRIMARY)
        paused_cb.pack(side=tk.LEFT)
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg=Colors.BG_PRIMARY)
        button_frame.pack(fill=tk.X)
        
        cancel_btn = ModernButton(button_frame, text="Cancel", style_type="secondary",
                                command=self._cancel)
        cancel_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        save_text = "Update Task" if self.task_data else "Create Task"
        save_btn = ModernButton(button_frame, text=save_text, style_type="success",
                              command=self._save)
        save_btn.pack(side=tk.RIGHT)
    
    def _set_today(self):
        today = datetime.now()
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, today.strftime("%Y-%m-%d"))
        self.time_entry.delete(0, tk.END)
        self.time_entry.insert(0, "09:00")
    
    def _validate_form(self):
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showerror("Validation Error", "Task title is required.")
            return False
        return True
    
    def _save(self):
        if not self._validate_form():
            return
        
        title = self.title_entry.get().strip()
        description = self.description_text.get(1.0, tk.END).strip()
        priority = self.priority_var.get()
        completed = self.completed_var.get()
        paused = self.paused_var.get()
        
        # Handle due date
        due_date = None
        date_value = self.date_entry.get().strip()
        time_value = self.time_entry.get().strip()
        
        if date_value and date_value != "YYYY-MM-DD":
            time_str = time_value if time_value and time_value != "HH:MM" else "09:00"
            try:
                due_dt = datetime.strptime(f"{date_value} {time_str}", "%Y-%m-%d %H:%M")
                due_date = due_dt.isoformat()
            except ValueError:
                pass
        
        self.result = {
            "title": title,
            "description": description,
            "priority": priority,
            "completed": completed,
            "paused": paused
        }
        
        if due_date:
            self.result["due_date"] = due_date
        
        self.dialog.destroy()
    
    def _cancel(self):
        self.result = None
        self.dialog.destroy()
    
    def show(self):
        self.dialog.wait_window()
        return self.result

# ==============================================================================
# MAIN APPLICATION
# ==============================================================================

class TaskManagerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Personal Day Planner")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        self.root.configure(bg=Colors.BG_PRIMARY)
        
        # Initialize connection manager and API client
        self.connection_manager = ConnectionManager(connection_callback=self._on_connection_change)
        self.api_client = TaskAPIClient(self.connection_manager)
        
        # Application state
        self.tasks = []
        self.app_enabled = False
        
        self._create_widgets()
        self._setup_connection()
        
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _create_widgets(self):
        # Main container
        main_container = tk.Frame(self.root, bg=Colors.BG_PRIMARY)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Connection status bar
        self.status_bar = tk.Frame(main_container, bg=Colors.BG_SECONDARY, height=30)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = tk.Label(self.status_bar, text="Connecting...",
                                   font=(Fonts.FAMILY_DEFAULT, Fonts.SIZE_SMALL),
                                   fg=Colors.TEXT_SECONDARY, bg=Colors.BG_SECONDARY)
        self.status_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        self.status_indicator = tk.Label(self.status_bar, text="●", fg=Colors.WARNING,
                                       font=(Fonts.FAMILY_DEFAULT, Fonts.SIZE_SMALL),
                                       bg=Colors.BG_SECONDARY)
        self.status_indicator.pack(side=tk.LEFT)
        
        # Main content area
        content_frame = tk.Frame(main_container, bg=Colors.BG_PRIMARY)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = tk.Frame(content_frame, bg=Colors.BG_PRIMARY)
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 0))
        
        title_label = tk.Label(header_frame, text="Task Manager",
                              font=(Fonts.FAMILY_DEFAULT, Fonts.SIZE_TITLE, "bold"),
                              fg=Colors.TEXT_PRIMARY, bg=Colors.BG_PRIMARY)
        title_label.pack(side=tk.LEFT)
        
        # Action buttons
        button_frame = tk.Frame(header_frame, bg=Colors.BG_PRIMARY)
        button_frame.pack(side=tk.RIGHT)
        
        self.refresh_btn = ModernButton(button_frame, text="🔄 Refresh", style_type="secondary",
                                      command=self._refresh_tasks)
        self.refresh_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.create_btn = ModernButton(button_frame, text="+ New Task", style_type="success",
                                     command=self._create_task)
        self.create_btn.pack(side=tk.LEFT)
        
        # Task counter
        counter_frame = tk.Frame(content_frame, bg=Colors.BG_PRIMARY)
        counter_frame.pack(fill=tk.X, padx=20, pady=(10, 0))
        
        self.task_counter = tk.Label(counter_frame, text="No tasks",
                                   font=(Fonts.FAMILY_DEFAULT, Fonts.SIZE_SMALL),
                                   fg=Colors.TEXT_SECONDARY, bg=Colors.BG_PRIMARY)
        self.task_counter.pack(side=tk.LEFT)
        
        # Tasks container with scrollbar
        tasks_container = tk.Frame(content_frame, bg=Colors.BG_PRIMARY)
        tasks_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(15, 20))
        
        # Scrollable frame
        self.canvas = tk.Canvas(tasks_container, bg=Colors.BG_PRIMARY, highlightthickness=0)
        scrollbar = tk.Scrollbar(tasks_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=Colors.BG_PRIMARY)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        
        # Disabled overlay
        self.disabled_overlay = tk.Frame(self.root, bg=Colors.BG_SECONDARY)
        self.disabled_message = tk.Label(
            self.disabled_overlay,
            text="Connecting to server...\nPlease wait.",
            font=(Fonts.FAMILY_DEFAULT, Fonts.SIZE_LARGE, "bold"),
            fg=Colors.TEXT_SECONDARY,
            bg=Colors.BG_SECONDARY
        )
        self.disabled_message.pack(expand=True)
        
        # Initially disable the app
        self._disable_app("Connecting to server...")
    
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def _setup_connection(self):
        self.connection_manager.start_monitoring()
        threading.Thread(target=self._initial_connection_check, daemon=True).start()
    
    def _initial_connection_check(self):
        if self.connection_manager.wait_for_connection(max_attempts=5):
            self.root.after(0, lambda: self._on_connection_change(True))
        else:
            self.root.after(0, lambda: self._on_connection_change(False))
    
    def _on_connection_change(self, connected: bool):
        if connected:
            self.status_label.config(text="Connected to server")
            self.status_indicator.config(fg=Colors.CONNECTED)
            self._enable_app()
            self._refresh_tasks()
        else:
            self.status_label.config(text="Disconnected from server")
            self.status_indicator.config(fg=Colors.DISCONNECTED)
            self._disable_app("No connection to server")
    
    def _enable_app(self):
        self.app_enabled = True
        self.disabled_overlay.pack_forget()
        self.refresh_btn.configure(state="normal")
        self.create_btn.configure(state="normal")
    
    def _disable_app(self, message: str):
        self.app_enabled = False
        self.disabled_overlay.pack(fill=tk.BOTH, expand=True)
        self.disabled_message.config(text=message)
        self.refresh_btn.configure(state="disabled")
        self.create_btn.configure(state="disabled")
    
    def _refresh_tasks(self):
        if not self.app_enabled:
            return
        
        try:
            self.tasks = self.api_client.get_all_tasks()
            self._update_task_display()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load tasks: {str(e)}")
    
    def _create_task(self):
        if not self.app_enabled:
            return
        
        dialog = TaskFormDialog(self.root, title="Create New Task")
        result = dialog.show()
        
        if result:
            try:
                self.api_client.create_task(result)
                self._refresh_tasks()
                messagebox.showinfo("Success", "Task created successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create task: {str(e)}")
    
    def _edit_task(self, task_data):
        if not self.app_enabled:
            return
        
        dialog = TaskFormDialog(self.root, task_data=task_data, title="Edit Task")
        result = dialog.show()
        
        if result:
            try:
                self.api_client.update_task(task_data["id"], result)
                self._refresh_tasks()
                messagebox.showinfo("Success", "Task updated successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update task: {str(e)}")
    
    def _delete_task(self, task_data):
        if not self.app_enabled:
            return
        
        if messagebox.askyesno("Confirm Delete", 
                              f"Are you sure you want to delete '{task_data['title']}'?"):
            try:
                self.api_client.delete_task(task_data["id"])
                self._refresh_tasks()
                messagebox.showinfo("Success", "Task deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete task: {str(e)}")
    
    def _toggle_task(self, task_data):
        if not self.app_enabled:
            return
        
        try:
            if task_data.get("completed"):
                update_data = {"completed": False, "paused": False}
                message = "Task marked as incomplete"
            elif task_data.get("paused"):
                update_data = {"paused": False}
                message = "Task resumed"
            else:
                update_data = {"completed": True, "paused": False}
                message = "Task completed"
            
            self.api_client.update_task(task_data["id"], update_data)
            self._refresh_tasks()
            messagebox.showinfo("Success", message)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update task: {str(e)}")
    
    def _update_task_display(self):
        # Clear existing task cards
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Update counter
        task_count = len(self.tasks)
        if task_count == 0:
            self.task_counter.config(text="No tasks")
        else:
            self.task_counter.config(text=f"{task_count} tasks")
        
        # Create task cards
        if not self.tasks:
            no_tasks_label = tk.Label(
                self.scrollable_frame,
                text="Create your first task!",
                font=(Fonts.FAMILY_DEFAULT, Fonts.SIZE_MEDIUM),
                fg=Colors.TEXT_SECONDARY,
                bg=Colors.BG_PRIMARY
            )
            no_tasks_label.pack(pady=20)
        else:
            # Sort tasks by priority (high to low)
            sorted_tasks = sorted(self.tasks, key=lambda x: -x.get("priority", 0))
            
            for task in sorted_tasks:
                card = TaskCard(
                    self.scrollable_frame,
                    task,
                    on_edit=self._edit_task,
                    on_delete=self._delete_task,
                    on_toggle=self._toggle_task
                )
                card.pack(fill=tk.X, pady=(0, 10))
    
    def _on_closing(self):
        self.connection_manager.stop_monitoring()
        self.root.quit()
        self.root.destroy()
    
    def run(self):
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self._on_closing()

# ==============================================================================
# MAIN ENTRY POINT
# ==============================================================================

def main():
    try:
        # Check for requests library
        import requests
        
        # Create and run application
        app = TaskManagerApp()
        app.run()
        
    except ImportError:
        print("Error: requests library is required")
        print("Please install it with: pip install requests")
        sys.exit(1)
    except Exception as e:
        print(f"Application Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()