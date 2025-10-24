"""
iOS-style UI components for better visual design
"""

import tkinter as tk
from tkinter import ttk

class IOSCard(ttk.Frame):
    """Creates an iOS-style card with rounded appearance simulation"""
    
    def __init__(self, parent, **kwargs):
        # Extract custom options
        padding = kwargs.pop('card_padding', 20)
        
        # Create the card frame
        super().__init__(parent, style="Card.TFrame", **kwargs)
        
        # Add internal padding
        self.configure(padding=padding)
        
        # Configure grid weights for proper expansion
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

class IOSSection(ttk.LabelFrame):
    """iOS-style section with clean header"""
    
    def __init__(self, parent, text="", **kwargs):
        super().__init__(parent, text=text, style="TLabelFrame", **kwargs)
        
        # Add padding for iOS feel
        self.configure(padding=16)

class IOSButton(ttk.Button):
    """iOS-style button with proper styling"""
    
    def __init__(self, parent, style_type="primary", **kwargs):
        # Map style types to actual styles
        style_map = {
            "primary": "TButton",
            "secondary": "Secondary.TButton", 
            "success": "Success.TButton",
            "warning": "Warning.TButton",
            "danger": "Danger.TButton",
            "dashed": "Dashed.TButton"
        }
        
        style = kwargs.pop('style', style_map.get(style_type, "TButton"))
        super().__init__(parent, style=style, **kwargs)

def create_ios_layout(parent):
    """Create iOS-style layout structure"""
    # Main container with iOS background
    container = ttk.Frame(parent, style="Container.TFrame")
    container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=16, pady=16)
    
    # Configure container expansion
    container.grid_columnconfigure(0, weight=1)
    
    return container

def add_shadow_effect(widget):
    """Simulate shadow effect with colored frames (limited in tkinter)"""
    # This is a basic shadow simulation - real shadows would need a different UI framework
    shadow_frame = tk.Frame(widget.master, bg='#e0e0e0', height=2)
    
    # Get widget's grid info to place shadow
    info = widget.grid_info()
    if info:
        shadow_frame.grid(
            row=info['row'] + 1, 
            column=info['column'], 
            sticky=(tk.W, tk.E),
            columnspan=info.get('columnspan', 1)
        )
    
    return shadow_frame