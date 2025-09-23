import tkinter as tk
from tkinter import ttk
from datetime import datetime
from .modern_styles import ModernStyles

class ModernTaskList:
    def __init__(self, parent, on_task_select=None, on_task_update=None):
        self.parent = parent
        self.on_task_select = on_task_select
        self.on_task_update = on_task_update
        self.tasks = []
        self.item_to_task = {}  # Map treeview item IDs to task data
        self.setup_ui()
    
    def setup_ui(self):
        # Main container frame
        self.main_frame = tk.Frame(self.parent, **ModernStyles.get_frame_style('primary'))
        self.main_frame.pack(fill='both', expand=True, padx=ModernStyles.SPACING['medium'], 
                            pady=ModernStyles.SPACING['medium'])
        
        # Header section
        self.create_header()
        
        # Task list section
        self.create_task_list()
        
        # Action buttons section
        self.create_action_buttons()
    
    def create_header(self):
        header_frame = tk.Frame(self.main_frame, **ModernStyles.get_frame_style('secondary'))
        header_frame.pack(fill='x', pady=(0, ModernStyles.SPACING['medium']))
        
        # Title
        title_label = tk.Label(header_frame, text="Task Management", 
                              **ModernStyles.get_label_style('title'))
        title_label.pack(side='left', padx=ModernStyles.SPACING['medium'], 
                        pady=ModernStyles.SPACING['medium'])
        
        # Task count
        self.count_label = tk.Label(header_frame, text="0 tasks", 
                                   **ModernStyles.get_label_style('small'))
        self.count_label.pack(side='right', padx=ModernStyles.SPACING['medium'], 
                             pady=ModernStyles.SPACING['medium'])
    
    def create_task_list(self):
        # Create container with scrollbar
        list_container = tk.Frame(self.main_frame, **ModernStyles.get_frame_style('secondary'))
        list_container.pack(fill='both', expand=True, pady=(0, ModernStyles.SPACING['medium']))
        
        # Configure treeview style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors for dark theme
        style.configure('Modern.Treeview',
                       background=ModernStyles.COLORS['bg_secondary'],
                       foreground=ModernStyles.COLORS['text_primary'],
                       fieldbackground=ModernStyles.COLORS['bg_secondary'],
                       borderwidth=0,
                       font=ModernStyles.FONTS['body'])
        
        style.configure('Modern.Treeview.Heading',
                       background=ModernStyles.COLORS['bg_tertiary'],
                       foreground=ModernStyles.COLORS['text_primary'],
                       font=ModernStyles.FONTS['heading'],
                       relief='flat')
        
        style.map('Modern.Treeview',
                 background=[('selected', ModernStyles.COLORS['accent_blue'])],
                 foreground=[('selected', ModernStyles.COLORS['text_primary'])])
        
        # Create treeview
        columns = ('Title', 'Priority', 'Status', 'Due Date')
        self.tree = ttk.Treeview(list_container, columns=columns, show='headings',
                                style='Modern.Treeview', height=15)
        
        # Configure columns
        self.tree.heading('Title', text='Title')
        self.tree.heading('Priority', text='Priority')
        self.tree.heading('Status', text='Status')
        self.tree.heading('Due Date', text='Due Date')
        
        self.tree.column('Title', width=300, minwidth=200)
        self.tree.column('Priority', width=80, minwidth=60, anchor='center')
        self.tree.column('Status', width=100, minwidth=80, anchor='center')
        self.tree.column('Due Date', width=120, minwidth=100, anchor='center')
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(list_container, orient='vertical', command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(list_container, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Bind events
        self.tree.bind('<Double-1>', self.on_item_double_click)
        self.tree.bind('<Button-3>', self.show_context_menu)  # Right click
    
    def create_action_buttons(self):
        button_frame = tk.Frame(self.main_frame, **ModernStyles.get_frame_style('primary'))
        button_frame.pack(fill='x')
        
        # Quick action buttons
        buttons_data = [
            ('Refresh', 'secondary', self.refresh_tasks),
            ('Mark Complete', 'success', self.mark_complete),
            ('Mark Paused', 'warning', self.mark_paused),
            ('Delete', 'danger', self.delete_task),
        ]
        
        for text, style, command in buttons_data:
            btn = tk.Button(button_frame, text=text, command=command,
                           **ModernStyles.get_button_style(style))
            btn.pack(side='left', padx=(0, ModernStyles.SPACING['small']),
                    ipadx=ModernStyles.SPACING['medium'])
    
    def update_tasks(self, tasks):
        """Update the task list display"""
        self.tasks = tasks
        
        # Clear existing items and mapping
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.item_to_task.clear()
        
        # Add tasks to treeview
        for task in tasks:
            status = self.get_task_status(task)
            due_date = self.format_due_date(task.get('due_date'))
            priority = f"{task.get('priority', 0):.0f}"
            
            # Insert with task data
            item_id = self.tree.insert('', 'end', values=(
                task.get('title', 'Untitled'),
                priority,
                status,
                due_date
            ))
            
            # Store task data mapping
            self.item_to_task[item_id] = task
        
        # Update count
        self.count_label.config(text=f"{len(tasks)} tasks")
    
    def get_task_status(self, task):
        """Get formatted task status"""
        if task.get('completed', False):
            return "✓ Complete"
        elif task.get('paused', False):
            return "⏸ Paused"
        else:
            return "⏵ Active"
    
    def format_due_date(self, due_date):
        """Format due date for display"""
        if not due_date:
            return "-"
        
        try:
            if isinstance(due_date, str):
                # Parse ISO format
                dt = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
            else:
                dt = due_date
            
            # Format as MM/DD
            return dt.strftime('%m/%d')
        except:
            return "-"
    
    def get_selected_task(self):
        """Get the currently selected task"""
        selection = self.tree.selection()
        if not selection:
            return None
        
        item_id = selection[0]
        return self.item_to_task.get(item_id, None)
    
    def on_item_double_click(self, event):
        """Handle double-click on task item"""
        task = self.get_selected_task()
        if task and self.on_task_select:
            self.on_task_select(task)
    
    def show_context_menu(self, event):
        """Show right-click context menu"""
        # Select the item under cursor
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            
            # Create context menu
            context_menu = tk.Menu(self.parent, tearoff=0,
                                 bg=ModernStyles.COLORS['bg_tertiary'],
                                 fg=ModernStyles.COLORS['text_primary'],
                                 activebackground=ModernStyles.COLORS['accent_blue'])
            
            context_menu.add_command(label="Edit Task", command=self.edit_selected_task)
            context_menu.add_separator()
            context_menu.add_command(label="Mark Complete", command=self.mark_complete)
            context_menu.add_command(label="Mark Paused", command=self.mark_paused)
            context_menu.add_separator()
            context_menu.add_command(label="Delete Task", command=self.delete_task)
            
            try:
                context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                context_menu.grab_release()
    
    def edit_selected_task(self):
        """Edit the selected task"""
        task = self.get_selected_task()
        if task and self.on_task_select:
            self.on_task_select(task)
    
    def refresh_tasks(self):
        """Refresh task list"""
        if self.on_task_update:
            self.on_task_update('refresh')
    
    def mark_complete(self):
        """Mark selected task as complete"""
        task = self.get_selected_task()
        if task and self.on_task_update:
            self.on_task_update('complete', task)
    
    def mark_paused(self):
        """Mark selected task as paused"""
        task = self.get_selected_task()
        if task and self.on_task_update:
            self.on_task_update('pause', task)
    
    def delete_task(self):
        """Delete selected task"""
        task = self.get_selected_task()
        if task and self.on_task_update:
            self.on_task_update('delete', task)