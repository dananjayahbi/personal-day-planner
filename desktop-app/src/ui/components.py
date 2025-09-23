"""
Custom UI Components for Personal Day Planner Desktop App
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
try:
    from .styles import *
except ImportError:
    try:
        from styles import *
    except ImportError:
        from ui.styles import *


class ModernButton(tk.Button):
    """Modern styled button with hover effects"""
    
    def __init__(self, parent, style_type="primary", **kwargs):
        """
        Initialize modern button
        
        Args:
            parent: Parent widget
            style_type: Button style (primary, secondary, success, danger)
            **kwargs: Additional button options
        """
        style_map = {
            "primary": Styles.BUTTON_PRIMARY,
            "secondary": Styles.BUTTON_SECONDARY,
            "success": Styles.BUTTON_SUCCESS,
            "danger": Styles.BUTTON_DANGER
        }
        
        style = style_map.get(style_type, Styles.BUTTON_PRIMARY)
        
        # Merge style with kwargs
        config = {**style, **kwargs}
        super().__init__(parent, **config)
        
        # Add hover effects
        normal_bg = config["bg"]
        if style_type == "primary":
            hover_bg = Colors.PRIMARY_DARK
        elif style_type == "secondary":
            hover_bg = Colors.SECONDARY_DARK
        elif style_type == "success":
            hover_bg = "#16a34a"  # Darker green
        elif style_type == "danger":
            hover_bg = "#dc2626"  # Darker red
        else:
            hover_bg = Colors.PRIMARY_DARK
        
        apply_hover_effect(self, normal_bg, hover_bg)


class ModernEntry(tk.Entry):
    """Modern styled entry widget with placeholder support"""
    
    def __init__(self, parent, placeholder="", **kwargs):
        """
        Initialize modern entry
        
        Args:
            parent: Parent widget
            placeholder: Placeholder text
            **kwargs: Additional entry options
        """
        config = {**Styles.ENTRY_DEFAULT, **kwargs}
        super().__init__(parent, **config)
        
        self.placeholder = placeholder
        self.placeholder_color = Colors.TEXT_LIGHT
        self.normal_color = config.get("fg", Colors.TEXT_PRIMARY)
        
        if placeholder:
            self.insert(0, placeholder)
            self.config(fg=self.placeholder_color)
            
            self.bind("<FocusIn>", self._on_focus_in)
            self.bind("<FocusOut>", self._on_focus_out)
    
    def _on_focus_in(self, event):
        """Handle focus in event"""
        if self.get() == self.placeholder:
            self.delete(0, tk.END)
            self.config(fg=self.normal_color)
    
    def _on_focus_out(self, event):
        """Handle focus out event"""
        if not self.get():
            self.insert(0, self.placeholder)
            self.config(fg=self.placeholder_color)
    
    def get_value(self):
        """Get entry value, returns empty string if placeholder is shown"""
        value = self.get()
        return "" if value == self.placeholder else value


class ModernText(tk.Text):
    """Modern styled text widget with placeholder support"""
    
    def __init__(self, parent, placeholder="", **kwargs):
        """
        Initialize modern text widget
        
        Args:
            parent: Parent widget
            placeholder: Placeholder text
            **kwargs: Additional text options
        """
        config = {**Styles.TEXT_DEFAULT, **kwargs}
        super().__init__(parent, **config)
        
        self.placeholder = placeholder
        self.placeholder_color = Colors.TEXT_LIGHT
        self.normal_color = config.get("fg", Colors.TEXT_PRIMARY)
        
        if placeholder:
            self.insert(1.0, placeholder)
            self.config(fg=self.placeholder_color)
            
            self.bind("<FocusIn>", self._on_focus_in)
            self.bind("<FocusOut>", self._on_focus_out)
    
    def _on_focus_in(self, event):
        """Handle focus in event"""
        if self.get(1.0, tk.END).strip() == self.placeholder:
            self.delete(1.0, tk.END)
            self.config(fg=self.normal_color)
    
    def _on_focus_out(self, event):
        """Handle focus out event"""
        if not self.get(1.0, tk.END).strip():
            self.insert(1.0, self.placeholder)
            self.config(fg=self.placeholder_color)
    
    def get_value(self):
        """Get text value, returns empty string if placeholder is shown"""
        value = self.get(1.0, tk.END).strip()
        return "" if value == self.placeholder else value


class TaskCard(tk.Frame):
    """Custom task card widget"""
    
    def __init__(self, parent, task_data, on_edit=None, on_delete=None, on_toggle=None, **kwargs):
        """
        Initialize task card
        
        Args:
            parent: Parent widget
            task_data: Task data dictionary
            on_edit: Callback for edit action
            on_delete: Callback for delete action
            on_toggle: Callback for toggle complete/pause
            **kwargs: Additional frame options
        """
        config = {**Styles.FRAME_CARD, **kwargs}
        super().__init__(parent, **config)
        
        self.task_data = task_data
        self.on_edit = on_edit
        self.on_delete = on_delete
        self.on_toggle = on_toggle
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create card widgets"""
        # Main container
        main_frame = tk.Frame(self, **Styles.FRAME_DEFAULT)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=Spacing.PAD_MEDIUM, pady=Spacing.PAD_MEDIUM)
        
        # Header frame
        header_frame = tk.Frame(main_frame, **Styles.FRAME_DEFAULT)
        header_frame.pack(fill=tk.X, pady=(0, Spacing.PAD_SMALL))
        
        # Title
        title_label = tk.Label(header_frame, text=self.task_data.get("title", ""), **Styles.LABEL_HEADER)
        title_label.pack(side=tk.LEFT)
        
        # Priority indicator
        priority = self.task_data.get("priority", 0)
        priority_color = get_priority_color(priority)
        priority_frame = tk.Frame(header_frame, bg=priority_color, width=20, height=20)
        priority_frame.pack(side=tk.RIGHT, padx=(Spacing.PAD_SMALL, 0))
        priority_frame.pack_propagate(False)
        
        priority_label = tk.Label(priority_frame, text=f"{int(priority)}", 
                                fg=Colors.TEXT_WHITE, bg=priority_color,
                                font=(Fonts.FAMILY_DEFAULT, Fonts.SIZE_SMALL, Fonts.WEIGHT_BOLD))
        priority_label.pack(expand=True)
        
        # Description
        description = self.task_data.get("description", "")
        if description and len(description) > 100:
            description = description[:100] + "..."
        
        if description:
            desc_label = tk.Label(main_frame, text=description, **Styles.LABEL_NORMAL)
            desc_label.pack(fill=tk.X, pady=(0, Spacing.PAD_SMALL))
        
        # Status frame
        status_frame = tk.Frame(main_frame, **Styles.FRAME_DEFAULT)
        status_frame.pack(fill=tk.X, pady=(0, Spacing.PAD_SMALL))
        
        # Status indicators
        completed = self.task_data.get("completed", False)
        paused = self.task_data.get("paused", False)
        
        if completed:
            status_label = tk.Label(status_frame, text="✓ Completed", 
                                  fg=Colors.SUCCESS, **Styles.LABEL_SECONDARY)
            status_label.pack(side=tk.LEFT)
        elif paused:
            status_label = tk.Label(status_frame, text="⏸ Paused", 
                                  fg=Colors.WARNING, **Styles.LABEL_SECONDARY)
            status_label.pack(side=tk.LEFT)
        else:
            status_label = tk.Label(status_frame, text="⏵ Active", 
                                  fg=Colors.INFO, **Styles.LABEL_SECONDARY)
            status_label.pack(side=tk.LEFT)
        
        # Due date
        due_date = self.task_data.get("due_date")
        if due_date:
            try:
                due_dt = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
                due_str = due_dt.strftime("%m/%d/%Y %H:%M")
                due_label = tk.Label(status_frame, text=f"Due: {due_str}", **Styles.LABEL_SECONDARY)
                due_label.pack(side=tk.RIGHT)
            except:
                pass
        
        # Button frame
        button_frame = tk.Frame(main_frame, **Styles.FRAME_DEFAULT)
        button_frame.pack(fill=tk.X)
        
        # Action buttons
        if self.on_edit:
            edit_btn = ModernButton(button_frame, text="Edit", style_type="secondary",
                                  command=lambda: self.on_edit(self.task_data))
            edit_btn.pack(side=tk.LEFT, padx=(0, Spacing.PAD_SMALL))
        
        if self.on_delete:
            delete_btn = ModernButton(button_frame, text="Delete", style_type="danger",
                                    command=lambda: self.on_delete(self.task_data))
            delete_btn.pack(side=tk.LEFT, padx=(0, Spacing.PAD_SMALL))
        
        if self.on_toggle:
            if completed:
                toggle_text = "Mark Incomplete"
                toggle_style = "secondary"
            elif paused:
                toggle_text = "Resume"
                toggle_style = "success"
            else:
                toggle_text = "Complete" if not paused else "Pause"
                toggle_style = "success" if not paused else "secondary"
            
            toggle_btn = ModernButton(button_frame, text=toggle_text, style_type=toggle_style,
                                    command=lambda: self.on_toggle(self.task_data))
            toggle_btn.pack(side=tk.RIGHT)


class ConnectionStatusBar(tk.Frame):
    """Connection status indicator"""
    
    def __init__(self, parent, **kwargs):
        """Initialize connection status bar"""
        config = {**Styles.FRAME_SECONDARY, **kwargs}
        super().__init__(parent, **config)
        
        self.status_label = tk.Label(self, text="Connecting...", **Styles.LABEL_SECONDARY)
        self.status_label.pack(side=tk.LEFT, padx=Spacing.PAD_SMALL)
        
        self.indicator = tk.Label(self, text="●", fg=Colors.WARNING, **Styles.LABEL_SECONDARY)
        self.indicator.pack(side=tk.LEFT)
        
        self.update_status(False)
    
    def update_status(self, connected: bool):
        """Update connection status display"""
        if connected:
            self.status_label.config(text="Connected to server")
            self.indicator.config(fg=Colors.CONNECTED)
        else:
            self.status_label.config(text="Disconnected from server")
            self.indicator.config(fg=Colors.DISCONNECTED)


class FilterPanel(tk.Frame):
    """Filter panel for tasks"""
    
    def __init__(self, parent, on_filter_change=None, **kwargs):
        """
        Initialize filter panel
        
        Args:
            parent: Parent widget
            on_filter_change: Callback when filters change
        """
        config = {**Styles.FRAME_SECONDARY, **kwargs}
        super().__init__(parent, **config)
        
        self.on_filter_change = on_filter_change
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create filter widgets"""
        # Title
        title_label = tk.Label(self, text="Filters", **Styles.LABEL_HEADER)
        title_label.pack(pady=(Spacing.PAD_MEDIUM, Spacing.PAD_SMALL))
        
        # Priority filter
        priority_frame = tk.Frame(self, **Styles.FRAME_SECONDARY)
        priority_frame.pack(fill=tk.X, padx=Spacing.PAD_MEDIUM, pady=Spacing.PAD_SMALL)
        
        tk.Label(priority_frame, text="Priority Range:", **Styles.LABEL_NORMAL).pack(anchor=tk.W)
        
        self.min_priority = tk.Scale(priority_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                                   **Styles.SCALE_DEFAULT)
        self.min_priority.pack(fill=tk.X, pady=(Spacing.PAD_SMALL, 0))
        self.min_priority.bind("<ButtonRelease-1>", self._on_filter_change)
        
        self.max_priority = tk.Scale(priority_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                                   **Styles.SCALE_DEFAULT)
        self.max_priority.set(100)
        self.max_priority.pack(fill=tk.X)
        self.max_priority.bind("<ButtonRelease-1>", self._on_filter_change)
        
        # Status filters
        status_frame = tk.Frame(self, **Styles.FRAME_SECONDARY)
        status_frame.pack(fill=tk.X, padx=Spacing.PAD_MEDIUM, pady=Spacing.PAD_SMALL)
        
        tk.Label(status_frame, text="Status:", **Styles.LABEL_NORMAL).pack(anchor=tk.W)
        
        self.show_all = tk.BooleanVar(value=True)
        self.show_completed = tk.BooleanVar(value=True)
        self.show_incomplete = tk.BooleanVar(value=True)
        self.show_paused = tk.BooleanVar(value=True)
        
        tk.Checkbutton(status_frame, text="Show All", variable=self.show_all,
                      command=self._on_show_all_change, **Styles.FRAME_SECONDARY).pack(anchor=tk.W)
        tk.Checkbutton(status_frame, text="Completed", variable=self.show_completed,
                      command=self._on_filter_change, **Styles.FRAME_SECONDARY).pack(anchor=tk.W)
        tk.Checkbutton(status_frame, text="Incomplete", variable=self.show_incomplete,
                      command=self._on_filter_change, **Styles.FRAME_SECONDARY).pack(anchor=tk.W)
        tk.Checkbutton(status_frame, text="Paused", variable=self.show_paused,
                      command=self._on_filter_change, **Styles.FRAME_SECONDARY).pack(anchor=tk.W)
        
        # Apply button
        apply_btn = ModernButton(self, text="Apply Filters", style_type="primary",
                               command=self._on_filter_change)
        apply_btn.pack(pady=Spacing.PAD_MEDIUM)
    
    def _on_show_all_change(self):
        """Handle show all checkbox change"""
        show_all = self.show_all.get()
        self.show_completed.set(show_all)
        self.show_incomplete.set(show_all)
        self.show_paused.set(show_all)
        self._on_filter_change()
    
    def _on_filter_change(self, event=None):
        """Handle filter change"""
        if self.on_filter_change:
            filters = {
                "min_priority": self.min_priority.get(),
                "max_priority": self.max_priority.get(),
                "show_completed": self.show_completed.get(),
                "show_incomplete": self.show_incomplete.get(),
                "show_paused": self.show_paused.get()
            }
            self.on_filter_change(filters)
    
    def get_filters(self):
        """Get current filter values"""
        return {
            "min_priority": self.min_priority.get(),
            "max_priority": self.max_priority.get(),
            "show_completed": self.show_completed.get(),
            "show_incomplete": self.show_incomplete.get(),
            "show_paused": self.show_paused.get()
        }