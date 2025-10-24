"""
Settings Dialog for Cambridge Report Card System
Allows modification of subject coefficients and other settings
"""

import tkinter as tk
from tkinter import ttk, messagebox
from config import CAMBRIDGE_SUBJECTS, update_subject_coefficient, reset_coefficients_to_default

class SettingsDialog:
    """Dialog for modifying application settings"""
    
    def __init__(self, parent):
        self.parent = parent
        self.result = None
        self.original_coefficients = {}
        
        # Store original coefficients for cancel functionality
        for subject in CAMBRIDGE_SUBJECTS:
            self.original_coefficients[subject["name"]] = subject["coefficient"]
        
        self.create_dialog()
    
    def create_dialog(self):
        """Create the settings dialog window"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Cambridge System Settings")
        self.dialog.resizable(True, True)
        self.dialog.configure(bg='#f8f9fa')  # Modern background
        
        # Apply modern styling to this dialog
        self.setup_modern_dialog_styles()
        
        # Make dialog modal
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Create the main frame
        main_frame = ttk.Frame(self.dialog, padding="15", style="Modern.TFrame")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.dialog.columnconfigure(0, weight=1)
        self.dialog.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Create widgets
        self.create_header(main_frame)
        self.create_coefficients_section(main_frame)
        self.create_buttons(main_frame)
        
        # Set proper size and center immediately
        self.setup_dialog_size()
        
        # Bind close event
        self.dialog.protocol("WM_DELETE_WINDOW", self.on_cancel)
    
    def setup_modern_dialog_styles(self):
        """Setup modern styling for the dialog"""
        style = ttk.Style()
        
        # Configure modern frame style
        style.configure("Modern.TFrame",
                       background='#ffffff',
                       relief="flat")
        
        # Configure modern button styles for dialog
        style.configure("Dialog.Primary.TButton",
                       background='#2563eb',
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       font=('Segoe UI', 10, 'bold'),
                       padding=(15, 8))
        
        style.configure("Dialog.Secondary.TButton",
                       background='#6b7280',
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       font=('Segoe UI', 10),
                       padding=(15, 8))
    
    def center_dialog(self):
        """Center the dialog on the parent window"""
        self.dialog.update_idletasks()
        
        # Get parent window position and size
        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        # Get dialog size
        dialog_width = self.dialog.winfo_reqwidth()
        dialog_height = self.dialog.winfo_reqheight()
        
        # Calculate position
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2
        
        self.dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
    
    def setup_dialog_size(self):
        """Setup proper dialog size and positioning"""
        # Set a good fixed size that shows all content
        width = 680
        height = 580
        
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
        self.dialog.minsize(650, 550)
    
    def create_header(self, parent):
        """Create the dialog header"""
        header_frame = ttk.LabelFrame(parent, text="Subject Coefficients", padding="10")
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        info_label = ttk.Label(
            header_frame,
            text="Modify the coefficient values for Cambridge subjects.\n"
                 "Coefficients determine the weight of each subject in final grade calculations.",
            font=('Arial', 9)
        )
        info_label.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        header_frame.columnconfigure(0, weight=1)
    
    def create_coefficients_section(self, parent):
        """Create the coefficients editing section"""
        coeff_frame = ttk.LabelFrame(parent, text="Edit Coefficients", padding="10")
        coeff_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Create treeview for editing coefficients
        columns = ('Subject', 'Current Coefficient', 'New Coefficient')
        self.coeff_tree = ttk.Treeview(coeff_frame, columns=columns, show='headings', height=12)
        
        # Configure columns
        self.coeff_tree.heading('Subject', text='Subject')
        self.coeff_tree.heading('Current Coefficient', text='Current Coefficient')
        self.coeff_tree.heading('New Coefficient', text='New Coefficient')
        
        # Set column widths
        self.coeff_tree.column('Subject', width=200)
        self.coeff_tree.column('Current Coefficient', width=150, anchor='center')
        self.coeff_tree.column('New Coefficient', width=150, anchor='center')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(coeff_frame, orient=tk.VERTICAL, command=self.coeff_tree.yview)
        self.coeff_tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid the widgets
        self.coeff_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Edit controls
        edit_frame = ttk.Frame(coeff_frame)
        edit_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Label(edit_frame, text="New Coefficient:").grid(row=0, column=0, padx=(0, 10))
        
        self.coeff_var = tk.StringVar()
        self.coeff_entry = ttk.Entry(edit_frame, textvariable=self.coeff_var, width=15)
        self.coeff_entry.grid(row=0, column=1, padx=(0, 10))
        
        self.update_btn = ttk.Button(
            edit_frame,
            text="Update Selected",
            command=self.update_selected_coefficient
        )
        self.update_btn.grid(row=0, column=2, padx=(0, 10))
        
        self.reset_btn = ttk.Button(
            edit_frame,
            text="Reset to Defaults",
            command=self.reset_to_defaults
        )
        self.reset_btn.grid(row=0, column=3)
        
        # Configure grid weights
        coeff_frame.columnconfigure(0, weight=1)
        coeff_frame.rowconfigure(0, weight=1)
        
        # Populate the treeview
        self.populate_coefficients()
        
        # Bind selection event
        self.coeff_tree.bind('<<TreeviewSelect>>', self.on_coefficient_select)
    
    def populate_coefficients(self):
        """Populate the coefficients treeview"""
        # Clear existing items
        for item in self.coeff_tree.get_children():
            self.coeff_tree.delete(item)
        
        # Add current coefficients
        for subject in CAMBRIDGE_SUBJECTS:
            self.coeff_tree.insert('', 'end', values=(
                subject["name"],
                f"{subject['coefficient']:.1f}",
                f"{subject['coefficient']:.1f}"
            ))
    
    def on_coefficient_select(self, event=None):
        """Handle coefficient selection"""
        selection = self.coeff_tree.selection()
        if selection:
            item = selection[0]
            values = self.coeff_tree.item(item, 'values')
            current_coeff = values[1]
            self.coeff_var.set(current_coeff)
    
    def update_selected_coefficient(self):
        """Update the selected coefficient"""
        selection = self.coeff_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a subject to update.")
            return
        
        try:
            new_coeff = float(self.coeff_var.get())
            if new_coeff <= 0:
                raise ValueError("Coefficient must be positive")
        except ValueError as e:
            messagebox.showerror("Invalid Input", f"Please enter a valid positive number.\nError: {e}")
            return
        
        # Update the coefficient
        item = selection[0]
        values = list(self.coeff_tree.item(item, 'values'))
        subject_name = values[0]
        
        # Update in memory
        update_subject_coefficient(subject_name, new_coeff)
        
        # Update treeview
        values[1] = f"{new_coeff:.1f}"
        values[2] = f"{new_coeff:.1f}"
        self.coeff_tree.item(item, values=values)
        
        messagebox.showinfo("Updated", f"Coefficient for {subject_name} updated to {new_coeff:.1f}")
    
    def reset_to_defaults(self):
        """Reset all coefficients to default values"""
        if messagebox.askyesno("Confirm Reset", 
                              "Are you sure you want to reset all coefficients to their default values?"):
            reset_coefficients_to_default()
            self.populate_coefficients()
            messagebox.showinfo("Reset Complete", "All coefficients have been reset to default values.")
    
    def create_buttons(self, parent):
        """Create dialog buttons"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(20, 0))
        
        # Configure the frame to push buttons to the right
        button_frame.columnconfigure(0, weight=1)
        
        ttk.Button(
            button_frame,
            text="✅ Apply Changes",
            command=self.on_ok,
            width=15,
            style="Dialog.Primary.TButton"
        ).grid(row=0, column=1, padx=(0, 15))
        
        ttk.Button(
            button_frame,
            text="❌ Cancel",
            command=self.on_cancel,
            width=12,
            style="Dialog.Secondary.TButton"
        ).grid(row=0, column=2)
    
    def on_ok(self):
        """Handle OK button"""
        self.result = True
        self.dialog.destroy()
    
    def on_cancel(self):
        """Handle Cancel button"""
        # Restore original coefficients
        for subject_name, original_coeff in self.original_coefficients.items():
            update_subject_coefficient(subject_name, original_coeff)
        
        self.result = False
        self.dialog.destroy()
    
    def show(self):
        """Show the dialog and return the result"""
        self.dialog.wait_window()
        return self.result

def show_settings_dialog(parent):
    """Show the settings dialog"""
    dialog = SettingsDialog(parent)
    return dialog.show()