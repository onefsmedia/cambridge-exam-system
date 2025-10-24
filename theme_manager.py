"""
Simple 3-Color Theme Manager for Cambridge Report Card System
Provides a clean, simple 3-color design
"""

import tkinter as tk
from tkinter import ttk
import json
import os
from typing import Dict, Any

class ThemeManager:
    """Manages application themes with simple 3-color system"""
    
    def __init__(self):
        self.current_theme = "simple"
        self.themes = self._initialize_themes()
        self.style = None
        
    def _initialize_themes(self) -> Dict[str, Dict[str, Any]]:
        """Initialize Apple-style theme"""
        return {
            "simple": {
                "name": "iOS Style",
                "description": "Clean iOS-inspired design",
                "colors": {
                    # iOS-style colors
                    'background': '#f2f2f7',      # iOS system background
                    'primary': '#007aff',         # iOS blue
                    'text': '#1d1d1f',            # iOS primary text
                    
                    # iOS color palette
                    'primary_light': '#007aff',
                    'primary_dark': '#0066cc', 
                    'secondary': '#007aff',
                    'accent': '#34c759',          # iOS green
                    'warning': '#ff9500',         # iOS orange
                    'danger': '#ff3b30',          # iOS red
                    'surface': '#ffffff',         # Pure white cards/surfaces
                    'border': '#e5e5ea',         # iOS subtle border
                    'text_primary': '#1d1d1f',
                    'text_secondary': '#8e8e93',  # iOS secondary text gray
                    'text_muted': '#8e8e93'
                }
            }
        }
    
    def get_available_themes(self) -> Dict[str, str]:
        """Get list of available themes with their display names"""
        return {theme_id: theme_data["name"] for theme_id, theme_data in self.themes.items()}
    
    def get_theme_description(self, theme_id: str) -> str:
        """Get description of a specific theme"""
        return self.themes.get(theme_id, {}).get("description", "No description available")
    
    def get_current_theme(self) -> str:
        """Get the current theme ID"""
        return self.current_theme
    
    def get_current_colors(self) -> Dict[str, str]:
        """Get colors for the current theme"""
        return self.themes[self.current_theme]["colors"]
    
    def set_theme(self, theme_id: str) -> bool:
        """Set the current theme"""
        if theme_id in self.themes:
            self.current_theme = theme_id
            self.save_theme_preference()
            return True
        return False
    
    def apply_theme_to_style(self, style: ttk.Style):
        """Apply Apple-style design"""
        self.style = style
        
        # Use default theme with Apple customizations
        style.theme_use('clam')
        
        # iOS-style frame and label configuration
        style.configure("TLabelFrame",
                       background='#ffffff',        # White card background for sections
                       borderwidth=0,               # No border for modern look
                       relief="flat")
        
        style.configure("TLabelFrame.Label",
                       background='#ffffff',
                       foreground='#1d1d1f',       
                       font=('SF Pro Display', 14, 'semibold'))  # iOS section header style
        
        # Modern iOS card-style frames with shadow simulation
        style.configure("Card.TFrame",              
                       background='#ffffff',        # Pure white card background
                       borderwidth=0,               # No visible border
                       relief="flat")               # Flat modern look
        
        # iOS-style content frames
        style.configure("TFrame",
                       background='#f2f2f7')        # iOS system background
        
        # Main container frame with iOS background
        style.configure("Container.TFrame",
                       background='#f2f2f7')
        
        style.configure("TLabel",
                       background='#f2f2f7',        # iOS system background
                       foreground='#1d1d1f',
                       font=('SF Pro Display', 11, 'normal'))
        
        # iOS-style title typography
        style.configure("Title.TLabel",
                       background='#f2f2f7',
                       foreground='#1d1d1f',       
                       font=('SF Pro Display', 22, 'bold'))  # Larger iOS title
        
        # iOS-style subtitle typography
        style.configure("Subtitle.TLabel",
                       background='#f2f2f7',
                       foreground='#8e8e93',       # iOS secondary text color
                       font=('SF Pro Display', 13, 'normal'))
        
        # Card content labels (white background for cards)
        style.configure("CardLabel.TLabel",
                       background='#ffffff',        # White for card content
                       foreground='#1d1d1f',
                       font=('SF Pro Display', 11, 'normal'))
        
        style.configure("TFrame",
                       background='#f5f5f7')
        
        # Modern iOS-style button design
        style.configure("TButton",
                       background='#007aff',       # iOS blue
                       foreground='#ffffff',
                       borderwidth=0,
                       relief="flat",
                       font=('SF Pro Display', 11, 'medium'),
                       padding=(24, 12),           # More generous padding for iOS feel
                       focuscolor='none')          # Remove focus outline
        
        style.map("TButton",
                 background=[('active', '#0066cc'),    # Darker blue on hover
                           ('pressed', '#004499'),     # Even darker when pressed
                           ('disabled', '#e5e5ea')],   # iOS disabled gray
                 foreground=[('disabled', '#8e8e93')]) # iOS disabled text
        
        # iOS-style entry fields with rounded appearance
        style.configure("TEntry",
                       fieldbackground='#ffffff',   
                       foreground='#1d1d1f',
                       borderwidth=1,
                       relief="solid",
                       bordercolor='#e5e5ea',      # iOS border color
                       insertcolor='#007aff',      
                       font=('SF Pro Display', 11, 'normal'),
                       padding=(16, 12))           # iOS-style generous padding
        
        style.map("TEntry",
                 bordercolor=[('focus', '#007aff')],   
                 fieldbackground=[('focus', '#ffffff')])
        
        # iOS-style combobox with matching styling
        style.configure("TCombobox",
                       fieldbackground='#ffffff',
                       foreground='#1d1d1f',
                       borderwidth=1,
                       relief="solid",
                       bordercolor='#e5e5ea',      # iOS border color
                       font=('SF Pro Display', 11, 'normal'),
                       padding=(16, 12))           # Match entry padding
        
        style.map("TCombobox",
                 bordercolor=[('focus', '#007aff')],
                 fieldbackground=[('focus', '#ffffff')])
        
        # Apple-style treeview/table
        style.configure("Treeview",
                       background='#ffffff',
                       foreground='#1d1d1f',
                       borderwidth=1,
                       relief="solid",
                       bordercolor='#d1d1d6',
                       font=('SF Pro Display', 11, 'normal'),
                       rowheight=28)              # Apple-style row height
        
        style.configure("Treeview.Heading",
                       background='#f5f5f7',       # Subtle header background
                       foreground='#1d1d1f',
                       borderwidth=1,
                       relief="solid",
                       bordercolor='#d1d1d6',
                       font=('SF Pro Display', 11, 'bold'))
        
        # iOS-style button variations
        style.configure("Success.TButton",
                       background='#34c759',       # iOS green
                       foreground='#ffffff',
                       borderwidth=0,
                       relief="flat",
                       font=('SF Pro Display', 11, 'medium'),
                       padding=(24, 12),
                       focuscolor='none')
        
        style.map("Success.TButton",
                 background=[('active', '#2fb149'),    
                           ('pressed', '#268e3f')])    
        
        style.configure("Warning.TButton", 
                       background='#ff9500',       # iOS orange
                       foreground='#ffffff',
                       borderwidth=0,
                       relief="flat",
                       font=('SF Pro Display', 11, 'medium'),
                       padding=(24, 12),
                       focuscolor='none')
        
        style.map("Warning.TButton",
                 background=[('active', '#e6850a'),    
                           ('pressed', '#cc750a')])    
        
        style.configure("Danger.TButton",
                       background='#ff3b30',       # iOS red
                       foreground='#ffffff',
                       borderwidth=0,
                       relief="flat",
                       font=('SF Pro Display', 11, 'medium'),
                       padding=(24, 12),
                       focuscolor='none')
        
        style.map("Danger.TButton",
                 background=[('active', '#e0342a'),    
                           ('pressed', '#c42d24')])    
        
        # Default/Secondary button style (like in the reference)
        style.configure("Secondary.TButton",
                       background='#ffffff',       # White background
                       foreground='#007aff',       # iOS blue text
                       borderwidth=1,
                       relief="solid",
                       bordercolor='#e5e5ea',      # iOS border
                       font=('SF Pro Display', 11, 'medium'),
                       padding=(24, 12),
                       focuscolor='none')
        
        style.map("Secondary.TButton",
                 background=[('active', '#f2f2f7'),    # Light gray on hover
                           ('pressed', '#e5e5ea')],    # Darker gray when pressed
                 bordercolor=[('active', '#007aff'),   # Blue border on hover
                            ('pressed', '#0066cc')])
        
        # Dashed button style (like in reference)
        style.configure("Dashed.TButton",
                       background='#ffffff',       
                       foreground='#8e8e93',       # iOS secondary text
                       borderwidth=1,
                       relief="solid",
                       bordercolor='#e5e5ea',      
                       font=('SF Pro Display', 11, 'normal'),
                       padding=(24, 12),
                       focuscolor='none')
        
        style.map("Dashed.TButton",
                 background=[('active', '#f2f2f7'),    
                           ('pressed', '#e5e5ea')],    
                 foreground=[('active', '#1d1d1f'),   # Darker text on hover
                           ('pressed', '#1d1d1f')])
    
    def get_theme_config_path(self) -> str:
        """Get path to theme configuration file"""
        return os.path.join(os.path.expanduser("~"), ".cambridge_theme.json")
    
    def save_theme_preference(self):
        """Save current theme preference to file"""
        try:
            config = {"current_theme": self.current_theme}
            with open(self.get_theme_config_path(), 'w') as f:
                json.dump(config, f)
        except Exception:
            pass  # Silently fail if can't save preference
    
    def load_theme_preference(self) -> str:
        """Load theme preference from file"""
        try:
            with open(self.get_theme_config_path(), 'r') as f:
                config = json.load(f)
                theme_id = config.get("current_theme", "simple")
                if theme_id in self.themes:
                    self.current_theme = theme_id
                    return theme_id
        except Exception:
            pass  # Silently fail if can't load preference
        return "simple"

# Global theme manager instance
theme_manager = ThemeManager()