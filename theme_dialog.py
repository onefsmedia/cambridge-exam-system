"""
Theme Selection Dialog for Cambridge Report Card System
Allows users to preview and select different color themes
"""

import tkinter as tk
from tkinter import ttk, messagebox
from theme_manager import theme_manager

class ThemeSelectionDialog:
    """Dialog for selecting application themes"""
    
    def __init__(self, parent, on_theme_change_callback=None):
        self.parent = parent
        self.on_theme_change_callback = on_theme_change_callback
        self.result = None
        self.original_theme = theme_manager.get_current_theme()
        self.preview_frames = {}
        
        self.create_dialog()
    
    def create_dialog(self):
        """Create the theme selection dialog window"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Choose Application Theme")
        self.dialog.resizable(True, True)
        self.dialog.configure(bg='#f8f9fa')
        
        # Make dialog modal
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Create the main frame
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.dialog.columnconfigure(0, weight=1)
        self.dialog.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Create widgets
        self.create_header(main_frame)
        self.create_theme_grid(main_frame)
        self.create_buttons(main_frame)
        
        # Set proper size and center
        self.setup_dialog_size()
        
        # Bind close event
        self.dialog.protocol("WM_DELETE_WINDOW", self.on_cancel)
    
    def create_header(self, parent):
        """Create the dialog header"""
        header_frame = ttk.LabelFrame(parent, text="Theme Selection", padding="15")
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        title_label = ttk.Label(
            header_frame,
            text="Choose Your Preferred Color Theme",
            font=('Segoe UI', 14, 'bold')
        )
        title_label.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        subtitle_label = ttk.Label(
            header_frame,
            text="Select a theme to customize the appearance of the Cambridge Report Card Generator",
            font=('Segoe UI', 10)
        )
        subtitle_label.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(8, 0))
        
        header_frame.columnconfigure(0, weight=1)
    
    def create_theme_grid(self, parent):
        """Create the theme selection grid"""
        grid_frame = ttk.LabelFrame(parent, text="Available Themes", padding="15")
        grid_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        
        # Create scrollable frame for themes
        canvas = tk.Canvas(grid_frame, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(grid_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        grid_frame.columnconfigure(0, weight=1)
        grid_frame.rowconfigure(0, weight=1)
        
        # Create theme preview cards
        self.create_theme_cards(scrollable_frame)
        
        # Configure canvas scrolling
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
    
    def create_theme_cards(self, parent):
        """Create theme preview cards"""
        themes = theme_manager.get_available_themes()
        current_theme = theme_manager.get_current_theme()
        
        row = 0
        col = 0
        max_cols = 2
        
        for theme_id, theme_name in themes.items():
            theme_colors = theme_manager.themes[theme_id]["colors"]
            description = theme_manager.get_theme_description(theme_id)
            
            # Create theme card frame
            card_frame = ttk.LabelFrame(parent, text=theme_name, padding="15")
            card_frame.grid(row=row, column=col, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
            
            # Theme description
            desc_label = ttk.Label(
                card_frame,
                text=description,
                font=('Segoe UI', 9),
                wraplength=250
            )
            desc_label.grid(row=0, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 15))
            
            # Color preview swatches
            swatch_frame = ttk.Frame(card_frame)
            swatch_frame.grid(row=1, column=0, columnspan=4, pady=(0, 15))
            
            swatch_colors = ['primary', 'secondary', 'accent', 'warning']
            for i, color_key in enumerate(swatch_colors):
                color_value = theme_colors.get(color_key, '#000000')
                swatch = tk.Frame(swatch_frame, bg=color_value, width=40, height=30, relief="solid", bd=1)
                swatch.grid(row=0, column=i, padx=2)
                swatch.grid_propagate(False)
                
                # Add color name label
                color_label = ttk.Label(swatch_frame, text=color_key.title(), font=('Segoe UI', 8))
                color_label.grid(row=1, column=i, padx=2)
            
            # Preview sample elements
            preview_frame = ttk.Frame(card_frame)
            preview_frame.grid(row=2, column=0, columnspan=4, pady=(0, 15))
            
            # Sample button in theme colors
            sample_btn = tk.Button(
                preview_frame,
                text="Sample Button",
                bg=theme_colors['primary'],
                fg='white',
                font=('Segoe UI', 9),
                relief="flat",
                padx=15,
                pady=5
            )
            sample_btn.grid(row=0, column=0, padx=(0, 10))
            
            # Sample entry
            sample_entry = tk.Entry(
                preview_frame,
                bg=theme_colors['background'],
                fg=theme_colors['text_primary'],
                font=('Segoe UI', 9),
                width=15
            )
            sample_entry.insert(0, "Sample Text")
            sample_entry.grid(row=0, column=1)
            
            # Selection radio button
            is_current = theme_id == current_theme
            select_btn = ttk.Button(
                card_frame,
                text="✓ Selected" if is_current else "Select Theme",
                command=lambda t=theme_id: self.select_theme(t),
                style="Accent.TButton" if is_current else "Primary.TButton"
            )
            select_btn.grid(row=3, column=0, columnspan=4, pady=(10, 0), sticky=(tk.W, tk.E))
            
            # Store reference for updating
            self.preview_frames[theme_id] = {
                'card_frame': card_frame,
                'select_btn': select_btn,
                'is_current': is_current
            }
            
            card_frame.columnconfigure(0, weight=1)
            parent.columnconfigure(col, weight=1)
            
            # Move to next position
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
    
    def select_theme(self, theme_id):
        """Select a theme and update preview"""
        # Apply theme temporarily
        theme_manager.set_theme(theme_id)
        
        # Update button states
        for tid, components in self.preview_frames.items():
            btn = components['select_btn']
            if tid == theme_id:
                btn.configure(text="✓ Selected", style="Accent.TButton")
            else:
                btn.configure(text="Select Theme", style="Primary.TButton")
        
        # Apply theme to parent application if callback provided
        if self.on_theme_change_callback:
            self.on_theme_change_callback()
    
    def create_buttons(self, parent):
        """Create dialog buttons"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(20, 0))
        
        # Configure the frame to push buttons to the right
        button_frame.columnconfigure(0, weight=1)
        
        ttk.Button(
            button_frame,
            text="✅ Apply Theme",
            command=self.on_ok,
            width=15,
            style="Primary.TButton"
        ).grid(row=0, column=1, padx=(0, 15))
        
        ttk.Button(
            button_frame,
            text="❌ Cancel",
            command=self.on_cancel,
            width=12,
            style="Secondary.TButton"
        ).grid(row=0, column=2)
        
        ttk.Button(
            button_frame,
            text="🔄 Reset to Default",
            command=self.reset_to_default,
            width=15,
            style="Warning.TButton"
        ).grid(row=0, column=3, padx=(15, 0))
    
    def reset_to_default(self):
        """Reset to default theme"""
        self.select_theme("modern_blue")
    
    def setup_dialog_size(self):
        """Setup proper dialog size and positioning"""
        # Set a good size for the theme dialog
        width = 800
        height = 700
        
        # Get parent window position for centering
        try:
            parent_x = self.parent.winfo_rootx()
            parent_y = self.parent.winfo_rooty()
            parent_width = self.parent.winfo_width()
            parent_height = self.parent.winfo_height()
            
            # Calculate centered position
            x = parent_x + (parent_width - width) // 2
            y = parent_y + (parent_height - height) // 2
            
            # Ensure dialog stays on screen
            x = max(50, x)
            y = max(50, y)
            
        except (tk.TclError, AttributeError):
            # If parent window info not available, center on screen
            x = (self.dialog.winfo_screenwidth() - width) // 2
            y = (self.dialog.winfo_screenheight() - height) // 2
        
        # Set the geometry and minimum size
        self.dialog.geometry(f"{width}x{height}+{x}+{y}")
        self.dialog.minsize(750, 650)
    
    def on_ok(self):
        """Handle OK button"""
        self.result = True
        theme_manager.save_theme_preference()
        self.dialog.destroy()
    
    def on_cancel(self):
        """Handle Cancel button"""
        # Restore original theme
        theme_manager.set_theme(self.original_theme)
        if self.on_theme_change_callback:
            self.on_theme_change_callback()
        
        self.result = False
        self.dialog.destroy()

def show_theme_dialog(parent, on_theme_change_callback=None):
    """Show theme selection dialog"""
    dialog = ThemeSelectionDialog(parent, on_theme_change_callback)
    parent.wait_window(dialog.dialog)
    return dialog.result