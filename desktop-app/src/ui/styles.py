"""
UI Styles and Theming for Personal Day Planner Desktop App
"""

class Colors:
    """Color palette for the application"""
    
    # Primary colors
    PRIMARY = "#2563eb"      # Blue
    PRIMARY_DARK = "#1d4ed8"
    PRIMARY_LIGHT = "#3b82f6"
    
    # Secondary colors
    SECONDARY = "#64748b"    # Gray
    SECONDARY_DARK = "#475569"
    SECONDARY_LIGHT = "#94a3b8"
    
    # Background colors
    BG_PRIMARY = "#ffffff"   # White
    BG_SECONDARY = "#f8fafc" # Light gray
    BG_DARK = "#1e293b"      # Dark gray
    
    # Status colors
    SUCCESS = "#22c55e"      # Green
    WARNING = "#f59e0b"      # Orange
    ERROR = "#ef4444"        # Red
    INFO = "#3b82f6"         # Blue
    
    # Text colors
    TEXT_PRIMARY = "#1e293b"
    TEXT_SECONDARY = "#64748b"
    TEXT_LIGHT = "#94a3b8"
    TEXT_WHITE = "#ffffff"
    
    # Priority colors
    PRIORITY_HIGH = "#ef4444"    # Red
    PRIORITY_MEDIUM = "#f59e0b"  # Orange
    PRIORITY_LOW = "#22c55e"     # Green
    
    # Connection status
    CONNECTED = "#22c55e"
    DISCONNECTED = "#ef4444"


class Fonts:
    """Font configurations"""
    
    # Font families
    FAMILY_DEFAULT = "Segoe UI"
    FAMILY_MONOSPACE = "Consolas"
    
    # Font sizes
    SIZE_LARGE = 16
    SIZE_MEDIUM = 12
    SIZE_SMALL = 10
    SIZE_TITLE = 20
    SIZE_HEADER = 14
    
    # Font weights
    WEIGHT_NORMAL = "normal"
    WEIGHT_BOLD = "bold"


class Spacing:
    """Spacing and sizing constants"""
    
    # Padding
    PAD_SMALL = 5
    PAD_MEDIUM = 10
    PAD_LARGE = 20
    PAD_XLARGE = 30
    
    # Margins
    MARGIN_SMALL = 5
    MARGIN_MEDIUM = 10
    MARGIN_LARGE = 20
    
    # Widget sizes
    BUTTON_HEIGHT = 35
    ENTRY_HEIGHT = 30
    LISTBOX_HEIGHT = 200
    
    # Window dimensions
    WINDOW_MIN_WIDTH = 800
    WINDOW_MIN_HEIGHT = 600
    WINDOW_DEFAULT_WIDTH = 1000
    WINDOW_DEFAULT_HEIGHT = 700


class Styles:
    """Complete style configurations for different UI elements"""
    
    # Button styles
    BUTTON_PRIMARY = {
        "bg": Colors.PRIMARY,
        "fg": Colors.TEXT_WHITE,
        "font": (Fonts.FAMILY_DEFAULT, Fonts.SIZE_MEDIUM, Fonts.WEIGHT_BOLD),
        "relief": "flat",
        "borderwidth": 0,
        "padx": Spacing.PAD_MEDIUM,
        "pady": Spacing.PAD_SMALL,
        "cursor": "hand2"
    }
    
    BUTTON_SECONDARY = {
        "bg": Colors.SECONDARY,
        "fg": Colors.TEXT_WHITE,
        "font": (Fonts.FAMILY_DEFAULT, Fonts.SIZE_MEDIUM),
        "relief": "flat",
        "borderwidth": 0,
        "padx": Spacing.PAD_MEDIUM,
        "pady": Spacing.PAD_SMALL,
        "cursor": "hand2"
    }
    
    BUTTON_SUCCESS = {
        "bg": Colors.SUCCESS,
        "fg": Colors.TEXT_WHITE,
        "font": (Fonts.FAMILY_DEFAULT, Fonts.SIZE_MEDIUM, Fonts.WEIGHT_BOLD),
        "relief": "flat",
        "borderwidth": 0,
        "padx": Spacing.PAD_MEDIUM,
        "pady": Spacing.PAD_SMALL,
        "cursor": "hand2"
    }
    
    BUTTON_DANGER = {
        "bg": Colors.ERROR,
        "fg": Colors.TEXT_WHITE,
        "font": (Fonts.FAMILY_DEFAULT, Fonts.SIZE_MEDIUM, Fonts.WEIGHT_BOLD),
        "relief": "flat",
        "borderwidth": 0,
        "padx": Spacing.PAD_MEDIUM,
        "pady": Spacing.PAD_SMALL,
        "cursor": "hand2"
    }
    
    # Label styles
    LABEL_TITLE = {
        "font": (Fonts.FAMILY_DEFAULT, Fonts.SIZE_TITLE, Fonts.WEIGHT_BOLD),
        "fg": Colors.TEXT_PRIMARY,
        "bg": Colors.BG_PRIMARY
    }
    
    LABEL_HEADER = {
        "font": (Fonts.FAMILY_DEFAULT, Fonts.SIZE_HEADER, Fonts.WEIGHT_BOLD),
        "fg": Colors.TEXT_PRIMARY,
        "bg": Colors.BG_PRIMARY
    }
    
    LABEL_NORMAL = {
        "font": (Fonts.FAMILY_DEFAULT, Fonts.SIZE_MEDIUM),
        "fg": Colors.TEXT_PRIMARY,
        "bg": Colors.BG_PRIMARY
    }
    
    LABEL_SECONDARY = {
        "font": (Fonts.FAMILY_DEFAULT, Fonts.SIZE_SMALL),
        "fg": Colors.TEXT_SECONDARY,
        "bg": Colors.BG_PRIMARY
    }
    
    # Entry styles
    ENTRY_DEFAULT = {
        "font": (Fonts.FAMILY_DEFAULT, Fonts.SIZE_MEDIUM),
        "bg": Colors.BG_PRIMARY,
        "fg": Colors.TEXT_PRIMARY,
        "relief": "solid",
        "borderwidth": 1,
        "insertbackground": Colors.TEXT_PRIMARY
    }
    
    # Text widget styles
    TEXT_DEFAULT = {
        "font": (Fonts.FAMILY_DEFAULT, Fonts.SIZE_MEDIUM),
        "bg": Colors.BG_PRIMARY,
        "fg": Colors.TEXT_PRIMARY,
        "relief": "solid",
        "borderwidth": 1,
        "wrap": "word",
        "insertbackground": Colors.TEXT_PRIMARY
    }
    
    # Frame styles
    FRAME_DEFAULT = {
        "bg": Colors.BG_PRIMARY,
        "relief": "flat",
        "borderwidth": 0
    }
    
    FRAME_SECONDARY = {
        "bg": Colors.BG_SECONDARY,
        "relief": "flat",
        "borderwidth": 0
    }
    
    FRAME_CARD = {
        "bg": Colors.BG_PRIMARY,
        "relief": "solid",
        "borderwidth": 1,
        "highlightbackground": Colors.SECONDARY_LIGHT,
        "highlightthickness": 1
    }
    
    # Listbox styles
    LISTBOX_DEFAULT = {
        "font": (Fonts.FAMILY_DEFAULT, Fonts.SIZE_MEDIUM),
        "bg": Colors.BG_PRIMARY,
        "fg": Colors.TEXT_PRIMARY,
        "selectbackground": Colors.PRIMARY_LIGHT,
        "selectforeground": Colors.TEXT_WHITE,
        "relief": "solid",
        "borderwidth": 1,
        "activestyle": "none"
    }
    
    # Scale styles
    SCALE_DEFAULT = {
        "bg": Colors.BG_PRIMARY,
        "fg": Colors.TEXT_PRIMARY,
        "highlightbackground": Colors.BG_PRIMARY,
        "troughcolor": Colors.BG_SECONDARY,
        "activebackground": Colors.PRIMARY,
        "sliderrelief": "flat",
        "font": (Fonts.FAMILY_DEFAULT, Fonts.SIZE_SMALL)
    }


def get_priority_color(priority: float) -> str:
    """
    Get color based on priority value
    
    Args:
        priority: Priority value (0-100)
        
    Returns:
        Color hex string
    """
    if priority >= 75:
        return Colors.PRIORITY_HIGH
    elif priority >= 50:
        return Colors.PRIORITY_MEDIUM
    else:
        return Colors.PRIORITY_LOW


def apply_hover_effect(widget, normal_bg: str, hover_bg: str):
    """
    Apply hover effect to a widget
    
    Args:
        widget: Tkinter widget
        normal_bg: Normal background color
        hover_bg: Hover background color
    """
    def on_enter(event):
        widget.configure(bg=hover_bg)
    
    def on_leave(event):
        widget.configure(bg=normal_bg)
    
    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)