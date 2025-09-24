import tkinter as tk
from tkinter import ttk
import threading
import time
from .modern_styles import ModernStyles

class LoadingIndicator:
    """Modern loading indicator with spinner and message"""
    
    def __init__(self, parent):
        self.parent = parent
        self.is_visible = False
        self.spinner_thread = None
        self.should_spin = False
        self.current_frame = 0
        self.spinner_frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        
        # Create overlay frame
        self.overlay = None
        self.spinner_label = None
        self.message_label = None
        
    def create_overlay(self):
        """Create the loading overlay"""
        if self.overlay:
            return
            
        # Semi-transparent overlay
        self.overlay = tk.Frame(self.parent, **ModernStyles.get_frame_style('primary'))
        self.overlay.configure(bg=ModernStyles.COLORS['bg_primary'])
        
        # Container for loading content
        content_frame = tk.Frame(self.overlay, **ModernStyles.get_frame_style('secondary'))
        content_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Spinner
        spinner_style = ModernStyles.get_label_style('body').copy()
        spinner_style['font'] = ('Segoe UI', 24)
        self.spinner_label = tk.Label(
            content_frame,
            text=self.spinner_frames[0],
            **spinner_style
        )
        self.spinner_label.pack(pady=(ModernStyles.SPACING['large'], ModernStyles.SPACING['small']))
        
        # Loading message
        self.message_label = tk.Label(
            content_frame,
            text="Loading...",
            **ModernStyles.get_label_style('body')
        )
        self.message_label.pack(pady=(0, ModernStyles.SPACING['large']))
        
    def show(self, message="Loading..."):
        """Show loading indicator with message"""
        if self.is_visible:
            return
            
        self.create_overlay()
        self.message_label.config(text=message)
        
        # Show overlay
        self.overlay.place(x=0, y=0, relwidth=1, relheight=1)
        self.is_visible = True
        
        # Start spinner animation
        self.should_spin = True
        self.spinner_thread = threading.Thread(target=self._animate_spinner, daemon=True)
        self.spinner_thread.start()
        
        # Update display
        self.parent.update_idletasks()
        
    def hide(self):
        """Hide loading indicator"""
        if not self.is_visible:
            return
            
        # Stop spinner
        self.should_spin = False
        
        # Hide overlay
        if self.overlay:
            self.overlay.place_forget()
            
        self.is_visible = False
        
        # Update display
        self.parent.update_idletasks()
        
    def _animate_spinner(self):
        """Animate the spinner in background thread"""
        while self.should_spin and self.is_visible:
            if self.spinner_label:
                # Update spinner frame on main thread
                self.parent.after(0, self._update_spinner_frame)
            time.sleep(0.1)  # 100ms delay between frames
            
    def _update_spinner_frame(self):
        """Update spinner frame (called on main thread)"""
        if self.spinner_label and self.should_spin:
            self.current_frame = (self.current_frame + 1) % len(self.spinner_frames)
            self.spinner_label.config(text=self.spinner_frames[self.current_frame])
            
    def update_message(self, message):
        """Update loading message"""
        if self.message_label and self.is_visible:
            self.message_label.config(text=message)
            self.parent.update_idletasks()

class ProgressDialog:
    """Modal progress dialog for longer operations"""
    
    def __init__(self, parent, title="Processing...", message="Please wait..."):
        self.parent = parent
        self.dialog = None
        self.progress_var = None
        self.progress_bar = None
        self.message_label = None
        self.title = title
        self.message = message
        
    def show(self):
        """Show progress dialog"""
        if self.dialog:
            return
            
        # Create modal dialog
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title(self.title)
        self.dialog.geometry("400x150")
        self.dialog.configure(bg=ModernStyles.COLORS['bg_primary'])
        self.dialog.resizable(False, False)
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Center dialog
        self._center_dialog()
        
        # Create content
        self._create_content()
        
    def _center_dialog(self):
        """Center dialog on parent window"""
        self.dialog.update_idletasks()
        x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - 200
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - 75
        self.dialog.geometry(f"400x150+{x}+{y}")
        
    def _create_content(self):
        """Create dialog content"""
        container = tk.Frame(self.dialog, **ModernStyles.get_frame_style('primary'))
        container.pack(fill='both', expand=True, padx=ModernStyles.SPACING['large'],
                      pady=ModernStyles.SPACING['large'])
        
        # Message
        self.message_label = tk.Label(
            container,
            text=self.message,
            **ModernStyles.get_label_style('body')
        )
        self.message_label.pack(pady=(0, ModernStyles.SPACING['large']))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            container,
            variable=self.progress_var,
            mode='indeterminate',
            length=350
        )
        self.progress_bar.pack(pady=(0, ModernStyles.SPACING['medium']))
        
        # Start progress animation
        self.progress_bar.start(10)
        
    def update_message(self, message):
        """Update progress message"""
        if self.message_label:
            self.message_label.config(text=message)
            self.dialog.update_idletasks()
            
    def update_progress(self, value):
        """Update progress value (0-100)"""
        if self.progress_bar:
            self.progress_bar.config(mode='determinate')
            self.progress_var.set(value)
            self.dialog.update_idletasks()
            
    def hide(self):
        """Hide progress dialog"""
        if self.dialog:
            self.dialog.destroy()
            self.dialog = None

def show_loading(parent, operation_func, message="Loading...", success_callback=None, error_callback=None):
    """
    Show loading indicator while performing operation
    
    Args:
        parent: Parent widget
        operation_func: Function to execute (should be callable)
        message: Loading message
        success_callback: Called with result on success
        error_callback: Called with error on failure
    """
    loader = LoadingIndicator(parent)
    
    def run_operation():
        try:
            # Show loading
            parent.after(0, lambda: loader.show(message))
            
            # Execute operation
            result = operation_func()
            
            # Hide loading
            parent.after(0, loader.hide)
            
            # Call success callback
            if success_callback:
                parent.after(0, lambda: success_callback(result))
                
        except Exception as e:
            # Hide loading
            parent.after(0, loader.hide)
            
            # Call error callback
            if error_callback:
                parent.after(0, lambda error=e: error_callback(error))
    
    # Run operation in background thread
    thread = threading.Thread(target=run_operation, daemon=True)
    thread.start()
    
    return loader