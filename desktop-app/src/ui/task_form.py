import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from .modern_styles import ModernStyles

class TaskForm:
    def __init__(self, parent, on_save=None, task_data=None):
        self.parent = parent
        self.on_save = on_save
        self.task_data = task_data
        self.window = None
        
    def show(self):
        self.create_form_window()
        if self.task_data:
            self.populate_form()
            
    def create_form_window(self):
        self.window = tk.Toplevel(self.parent)
        self.window.title("Create Task" if not self.task_data else "Edit Task")
        self.window.geometry("400x500")
        self.window.configure(bg=ModernStyles.COLORS['bg_primary'])
        self.window.resizable(False, False)
        self.window.transient(self.parent)
        self.window.grab_set()
        
        # Center window
        self.center_window()
        
        # Create form
        self.create_form_elements()
        
    def center_window(self):
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.window.winfo_screenheight() // 2) - (500 // 2)
        self.window.geometry(f"400x500+{x}+{y}")
        
    def create_form_elements(self):
        # Main container with modern styling
        container = tk.Frame(self.window, **ModernStyles.get_frame_style('primary'))
        container.pack(fill='both', expand=True, padx=ModernStyles.SPACING['large'], 
                      pady=ModernStyles.SPACING['large'])
        
        # Header
        header_frame = tk.Frame(container, **ModernStyles.get_frame_style('secondary'))
        header_frame.pack(fill='x', pady=(0, ModernStyles.SPACING['large']))
        
        title_text = "Create New Task" if not self.task_data else "Edit Task"
        title_label = tk.Label(header_frame, text=title_text, 
                              **ModernStyles.get_label_style('title'))
        title_label.pack(pady=ModernStyles.SPACING['medium'])
        
        # Form fields in a compact layout
        self.create_form_field(container, "Title *", 'entry', 'title_entry')
        self.create_form_field(container, "Description", 'text', 'description_text', height=3)
        
        # Priority and due date in one row
        row_frame = tk.Frame(container, **ModernStyles.get_frame_style('primary'))
        row_frame.pack(fill='x', pady=(0, ModernStyles.SPACING['medium']))
        
        # Priority (left side)
        priority_frame = tk.Frame(row_frame, **ModernStyles.get_frame_style('primary'))
        priority_frame.pack(side='left', fill='x', expand=True, padx=(0, ModernStyles.SPACING['small']))
        
        tk.Label(priority_frame, text="Priority", **ModernStyles.get_label_style('body')).pack(anchor='w')
        self.priority_entry = tk.Entry(priority_frame, **ModernStyles.get_entry_style())
        self.priority_entry.pack(fill='x', ipady=3)
        self.priority_entry.insert(0, "50")
        
        # Due date (right side)
        date_frame = tk.Frame(row_frame, **ModernStyles.get_frame_style('primary'))
        date_frame.pack(side='right', fill='x', expand=True, padx=(ModernStyles.SPACING['small'], 0))
        
        tk.Label(date_frame, text="Due Date", **ModernStyles.get_label_style('body')).pack(anchor='w')
        self.due_date_entry = tk.Entry(date_frame, **ModernStyles.get_entry_style())
        self.due_date_entry.pack(fill='x', ipady=3)
        self.due_date_entry.insert(0, "YYYY-MM-DD HH:MM")
        self.due_date_entry.bind('<FocusIn>', self.clear_placeholder)
        
        # Status checkboxes in compact row
        status_frame = tk.Frame(container, **ModernStyles.get_frame_style('primary'))
        status_frame.pack(fill='x', pady=ModernStyles.SPACING['medium'])
        
        tk.Label(status_frame, text="Status", **ModernStyles.get_label_style('body')).pack(anchor='w')
        
        checkbox_frame = tk.Frame(status_frame, **ModernStyles.get_frame_style('primary'))
        checkbox_frame.pack(fill='x', pady=(ModernStyles.SPACING['small'], 0))
        
        self.completed_var = tk.BooleanVar()
        self.paused_var = tk.BooleanVar()
        
        completed_cb = tk.Checkbutton(
            checkbox_frame,
            text="Completed",
            variable=self.completed_var,
            font=ModernStyles.FONTS['body'],
            bg=ModernStyles.COLORS['bg_primary'],
            fg=ModernStyles.COLORS['text_secondary'],
            selectcolor=ModernStyles.COLORS['bg_input'],
            activebackground=ModernStyles.COLORS['bg_primary']
        )
        completed_cb.pack(side='left', padx=(0, ModernStyles.SPACING['large']))
        
        paused_cb = tk.Checkbutton(
            checkbox_frame,
            text="Paused",
            variable=self.paused_var,
            font=ModernStyles.FONTS['body'],
            bg=ModernStyles.COLORS['bg_primary'],
            fg=ModernStyles.COLORS['text_secondary'],
            selectcolor=ModernStyles.COLORS['bg_input'],
            activebackground=ModernStyles.COLORS['bg_primary']
        )
        paused_cb.pack(side='left')
        
        # Action buttons
        self.create_action_buttons(container)
        
        # Focus on title entry
        self.title_entry.focus()
        
    def create_form_field(self, parent, label_text, field_type, attr_name, **kwargs):
        """Create a form field with label"""
        field_frame = tk.Frame(parent, **ModernStyles.get_frame_style('primary'))
        field_frame.pack(fill='x', pady=(0, ModernStyles.SPACING['medium']))
        
        # Label
        label = tk.Label(field_frame, text=label_text, **ModernStyles.get_label_style('body'))
        label.pack(anchor='w', pady=(0, ModernStyles.SPACING['small']))
        
        # Field
        if field_type == 'entry':
            field = tk.Entry(field_frame, **ModernStyles.get_entry_style())
            field.pack(fill='x', ipady=3)
        elif field_type == 'text':
            height = kwargs.get('height', 4)
            field = tk.Text(field_frame, height=height, **ModernStyles.get_text_style())
            field.pack(fill='x')
        
        setattr(self, attr_name, field)
        
    def create_action_buttons(self, parent):
        """Create action buttons"""
        button_frame = tk.Frame(parent, **ModernStyles.get_frame_style('primary'))
        button_frame.pack(fill='x', pady=(ModernStyles.SPACING['large'], 0))
        
        # Cancel button
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=self.cancel,
            **ModernStyles.get_button_style('secondary')
        )
        cancel_btn.pack(side='right', padx=(ModernStyles.SPACING['small'], 0),
                       ipadx=ModernStyles.SPACING['medium'], ipady=5)
        
        # Save button
        save_text = "Save Task" if not self.task_data else "Update Task"
        save_btn = tk.Button(
            button_frame,
            text=save_text,
            command=self.save_task,
            **ModernStyles.get_button_style('primary')
        )
        save_btn.pack(side='right', ipadx=ModernStyles.SPACING['medium'], ipady=5)
        
    def clear_placeholder(self, event):
        """Clear placeholder text on focus"""
        if self.due_date_entry.get() == "YYYY-MM-DD HH:MM":
            self.due_date_entry.delete(0, tk.END)
        
    def populate_form(self):
        """Populate form with existing task data"""
        if not self.task_data:
            return
            
        # Title
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, self.task_data.get('title', ''))
        
        # Description
        self.description_text.delete('1.0', tk.END)
        self.description_text.insert('1.0', self.task_data.get('description', ''))
        
        # Priority
        self.priority_entry.delete(0, tk.END)
        self.priority_entry.insert(0, str(self.task_data.get('priority', 50)))
        
        # Due date
        due_date = self.task_data.get('due_date', '')
        if due_date:
            try:
                if isinstance(due_date, str):
                    dt = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
                    formatted_date = dt.strftime('%Y-%m-%d %H:%M')
                    self.due_date_entry.delete(0, tk.END)
                    self.due_date_entry.insert(0, formatted_date)
            except:
                pass
        
        # Status
        self.completed_var.set(self.task_data.get('completed', False))
        self.paused_var.set(self.task_data.get('paused', False))
        
    def validate_form(self):
        """Validate form data"""
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showerror("Validation Error", "Title is required!")
            return False
            
        try:
            priority = float(self.priority_entry.get())
            if not (0 <= priority <= 100):
                messagebox.showerror("Validation Error", "Priority must be between 0 and 100!")
                return False
        except ValueError:
            messagebox.showerror("Validation Error", "Priority must be a valid number!")
            return False
            
        # Validate due date if provided
        due_date = self.due_date_entry.get().strip()
        if due_date and due_date != "YYYY-MM-DD HH:MM":
            try:
                datetime.strptime(due_date, '%Y-%m-%d %H:%M')
            except ValueError:
                messagebox.showerror("Validation Error", "Due date must be in format: YYYY-MM-DD HH:MM")
                return False
                
        return True
        
    def save_task(self):
        """Save the task"""
        if not self.validate_form():
            return
            
        # Collect form data
        task_data = {
            'title': self.title_entry.get().strip(),
            'description': self.description_text.get('1.0', tk.END).strip(),
            'priority': float(self.priority_entry.get()),
            'completed': self.completed_var.get(),
            'paused': self.paused_var.get()
        }
        
        # Add due date if provided
        due_date = self.due_date_entry.get().strip()
        if due_date and due_date != "YYYY-MM-DD HH:MM":
            try:
                dt = datetime.strptime(due_date, '%Y-%m-%d %H:%M')
                task_data['due_date'] = dt.isoformat()
            except:
                pass
        
        # Include task ID if editing
        if self.task_data and 'id' in self.task_data:
            task_data['id'] = self.task_data['id']
            
        # Call save callback
        if self.on_save:
            self.on_save(task_data)
            
        self.window.destroy()
        
    def cancel(self):
        """Cancel form"""
        self.window.destroy()