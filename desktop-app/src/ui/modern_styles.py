# Modern UI Styles - Inspired by clean, minimalistic design
class ModernStyles:
    # Color scheme inspired by modern apps
    COLORS = {
        # Main colors
        'bg_primary': '#2B2B2B',        # Dark background
        'bg_secondary': '#3C3C3C',      # Secondary background
        'bg_tertiary': '#4A4A4A',       # Tertiary background
        'bg_input': '#404040',          # Input background
        'bg_hover': '#505050',          # Hover state
        
        # Text colors
        'text_primary': '#FFFFFF',      # Primary text
        'text_secondary': '#CCCCCC',    # Secondary text
        'text_muted': '#999999',        # Muted text
        'text_success': '#4CAF50',      # Success text
        'text_warning': '#FF9800',      # Warning text
        'text_error': '#F44336',        # Error text
        
        # Accent colors
        'accent_blue': '#2196F3',       # Blue accent
        'accent_green': '#4CAF50',      # Green accent
        'accent_orange': '#FF9800',     # Orange accent
        'accent_red': '#F44336',        # Red accent
        
        # Border colors
        'border_light': '#555555',      # Light border
        'border_medium': '#666666',     # Medium border
        'border_dark': '#777777',       # Dark border
    }
    
    # Font configurations
    FONTS = {
        'title': ('Segoe UI', 14, 'bold'),
        'heading': ('Segoe UI', 12, 'bold'),
        'body': ('Segoe UI', 10),
        'small': ('Segoe UI', 9),
        'button': ('Segoe UI', 10, 'bold'),
    }
    
    # Spacing and dimensions
    SPACING = {
        'small': 5,
        'medium': 10,
        'large': 15,
        'xlarge': 20,
    }
    
    DIMENSIONS = {
        'button_height': 30,
        'input_height': 25,
        'section_padding': 10,
        'window_min_width': 800,
        'window_min_height': 600,
    }
    
    @classmethod
    def get_button_style(cls, style_type='primary'):
        """Get button style configuration"""
        styles = {
            'primary': {
                'bg': cls.COLORS['accent_blue'],
                'fg': cls.COLORS['text_primary'],
                'activebackground': cls.COLORS['bg_hover'],
                'relief': 'flat',
                'font': cls.FONTS['button'],
                'cursor': 'hand2'
            },
            'success': {
                'bg': cls.COLORS['accent_green'],
                'fg': cls.COLORS['text_primary'],
                'activebackground': cls.COLORS['bg_hover'],
                'relief': 'flat',
                'font': cls.FONTS['button'],
                'cursor': 'hand2'
            },
            'warning': {
                'bg': cls.COLORS['accent_orange'],
                'fg': cls.COLORS['text_primary'],
                'activebackground': cls.COLORS['bg_hover'],
                'relief': 'flat',
                'font': cls.FONTS['button'],
                'cursor': 'hand2'
            },
            'danger': {
                'bg': cls.COLORS['accent_red'],
                'fg': cls.COLORS['text_primary'],
                'activebackground': cls.COLORS['bg_hover'],
                'relief': 'flat',
                'font': cls.FONTS['button'],
                'cursor': 'hand2'
            },
            'secondary': {
                'bg': cls.COLORS['bg_tertiary'],
                'fg': cls.COLORS['text_primary'],
                'activebackground': cls.COLORS['bg_hover'],
                'relief': 'flat',
                'font': cls.FONTS['button'],
                'cursor': 'hand2'
            }
        }
        return styles.get(style_type, styles['primary'])
    
    @classmethod
    def get_entry_style(cls):
        """Get entry/input style configuration"""
        return {
            'bg': cls.COLORS['bg_input'],
            'fg': cls.COLORS['text_primary'],
            'insertbackground': cls.COLORS['text_primary'],
            'relief': 'flat',
            'font': cls.FONTS['body'],
            'highlightthickness': 1,
            'highlightcolor': cls.COLORS['accent_blue'],
            'highlightbackground': cls.COLORS['border_light']
        }
    
    @classmethod
    def get_text_style(cls):
        """Get text widget style configuration"""
        return {
            'bg': cls.COLORS['bg_input'],
            'fg': cls.COLORS['text_primary'],
            'insertbackground': cls.COLORS['text_primary'],
            'relief': 'flat',
            'font': cls.FONTS['body'],
            'highlightthickness': 1,
            'highlightcolor': cls.COLORS['accent_blue'],
            'highlightbackground': cls.COLORS['border_light'],
            'wrap': 'word'
        }
    
    @classmethod
    def get_label_style(cls, style_type='body'):
        """Get label style configuration"""
        styles = {
            'title': {
                'bg': cls.COLORS['bg_primary'],
                'fg': cls.COLORS['text_primary'],
                'font': cls.FONTS['title']
            },
            'heading': {
                'bg': cls.COLORS['bg_primary'],
                'fg': cls.COLORS['text_primary'],
                'font': cls.FONTS['heading']
            },
            'body': {
                'bg': cls.COLORS['bg_primary'],
                'fg': cls.COLORS['text_secondary'],
                'font': cls.FONTS['body']
            },
            'small': {
                'bg': cls.COLORS['bg_primary'],
                'fg': cls.COLORS['text_muted'],
                'font': cls.FONTS['small']
            },
            'success': {
                'bg': cls.COLORS['bg_primary'],
                'fg': cls.COLORS['text_success'],
                'font': cls.FONTS['body']
            },
            'warning': {
                'bg': cls.COLORS['bg_primary'],
                'fg': cls.COLORS['text_warning'],
                'font': cls.FONTS['body']
            },
            'error': {
                'bg': cls.COLORS['bg_primary'],
                'fg': cls.COLORS['text_error'],
                'font': cls.FONTS['body']
            }
        }
        return styles.get(style_type, styles['body'])
    
    @classmethod
    def get_frame_style(cls, style_type='primary'):
        """Get frame style configuration"""
        styles = {
            'primary': {
                'bg': cls.COLORS['bg_primary'],
                'relief': 'flat'
            },
            'secondary': {
                'bg': cls.COLORS['bg_secondary'],
                'relief': 'flat'
            },
            'tertiary': {
                'bg': cls.COLORS['bg_tertiary'],
                'relief': 'flat'
            }
        }
        return styles.get(style_type, styles['primary'])