"""
Subject Edit Dialog for Cambridge Report Card System
Allows editing of individual subject data
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from config import get_subject_names, get_subject_coefficient
from grade_calculator import CambridgeGradeCalculator

class SubjectEditDialog:
    """Dialog for editing subject information"""
    
    def __init__(self, parent, subject_data):
        self.parent = parent
        self.original_data = subject_data.copy()
        self.result = None
        self.calculator = CambridgeGradeCalculator()
        
        self.create_dialog()
        self.populate_data()
    
    def create_dialog(self):
        """Create the edit dialog window"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Edit Subject")
        self.dialog.resizable(True, True)
        
        # Make dialog modal
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Create the main frame
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.dialog.columnconfigure(0, weight=1)
        self.dialog.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Create widgets
        self.create_form_fields(main_frame)
        self.create_buttons(main_frame)
        
        # Set proper size and center immediately
        self.setup_dialog_size()
        
        # Configure grid weights
        self.dialog.columnconfigure(0, weight=1)
        self.dialog.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Create widgets
        self.create_form_fields(main_frame)
        self.create_buttons(main_frame)
        
        # Bind close event
        self.dialog.protocol("WM_DELETE_WINDOW", self.on_cancel)
    
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
        # Set a good fixed size for the edit dialog
        width = 520
        height = 450
        
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
        self.dialog.minsize(500, 400)
    
    def create_form_fields(self, parent):
        """Create form fields for editing"""
        # Subject selection
        ttk.Label(parent, text="Subject:").grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        self.subject_var = tk.StringVar()
        self.subject_combo = ttk.Combobox(
            parent,
            textvariable=self.subject_var,
            values=get_subject_names(),
            state="readonly",
            width=25
        )
        self.subject_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 10))
        self.subject_combo.bind('<<ComboboxSelected>>', self.on_subject_changed)
        
        # Coefficient display
        ttk.Label(parent, text="Coefficient:").grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        self.coefficient_var = tk.StringVar()
        coefficient_label = ttk.Label(parent, textvariable=self.coefficient_var, font=('Arial', 10, 'bold'))
        coefficient_label.grid(row=1, column=1, sticky=tk.W, pady=(0, 10))
        
        # Score input
        ttk.Label(parent, text="Raw Score (0-100):").grid(row=2, column=0, sticky=tk.W, pady=(0, 10))
        score_frame = ttk.Frame(parent)
        score_frame.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.score_var = tk.StringVar()
        self.score_entry = ttk.Entry(score_frame, textvariable=self.score_var, width=15)
        self.score_entry.grid(row=0, column=0, padx=(0, 10))
        
        # Grade display
        ttk.Label(score_frame, text="Grade:").grid(row=0, column=1, padx=(0, 5))
        self.grade_var = tk.StringVar()
        self.grade_label = ttk.Label(score_frame, textvariable=self.grade_var, font=('Arial', 10, 'bold'))
        self.grade_label.grid(row=0, column=2)
        
        # Bind score changes
        self.score_var.trace('w', self.on_score_changed)
        
        # Teacher comment
        ttk.Label(parent, text="Teacher Comment:").grid(row=3, column=0, sticky=(tk.W, tk.N), pady=(0, 10))
        self.comment_text = scrolledtext.ScrolledText(parent, height=8, width=40)
        self.comment_text.grid(row=3, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Configure row weight for comment expansion
        parent.rowconfigure(3, weight=1)
    
    def populate_data(self):
        """Populate the dialog with existing data"""
        self.subject_var.set(self.original_data['name'])
        self.coefficient_var.set(f"{self.original_data['coefficient']:.1f}")
        self.score_var.set(str(self.original_data['score']))
        self.grade_var.set(self.original_data['grade'])
        self.comment_text.insert("1.0", self.original_data['comment'])
    
    def on_subject_changed(self, event=None):
        """Handle subject selection change"""
        selected_subject = self.subject_var.get()
        if selected_subject:
            coefficient = get_subject_coefficient(selected_subject)
            self.coefficient_var.set(f"{coefficient:.1f}")
            self.calculate_grade()
    
    def on_score_changed(self, *args):
        """Handle score change"""
        self.calculate_grade()
    
    def calculate_grade(self):
        """Calculate and display the grade"""
        try:
            score = float(self.score_var.get())
            if 0 <= score <= 100:
                grade = self.calculator.score_to_grade(score)
                self.grade_var.set(grade)
            else:
                self.grade_var.set("Invalid range")
        except ValueError:
            self.grade_var.set("Invalid score")
    
    def create_buttons(self, parent):
        """Create dialog buttons"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=4, column=0, columnspan=2, pady=(20, 0), sticky=(tk.W, tk.E))
        
        # Configure the frame to center buttons
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(3, weight=1)
        
        ttk.Button(
            button_frame,
            text="OK",
            command=self.on_ok,
            width=10
        ).grid(row=0, column=1, padx=(0, 10))
        
        ttk.Button(
            button_frame,
            text="Cancel",
            command=self.on_cancel,
            width=10
        ).grid(row=0, column=2)
    
    def validate_data(self):
        """Validate the entered data"""
        # Check subject selection
        if not self.subject_var.get():
            messagebox.showerror("Validation Error", "Please select a subject.")
            return False
        
        # Check score
        try:
            score = float(self.score_var.get())
            if not (0 <= score <= 100):
                messagebox.showerror("Validation Error", "Score must be between 0 and 100.")
                return False
        except ValueError:
            messagebox.showerror("Validation Error", "Please enter a valid score.")
            return False
        
        return True
    
    def get_data(self):
        """Get the edited data"""
        subject_name = self.subject_var.get()
        coefficient = get_subject_coefficient(subject_name)
        score = float(self.score_var.get())
        grade = self.calculator.score_to_grade(score)
        weighted_score = score * coefficient
        comment = self.comment_text.get("1.0", tk.END).strip()
        
        return {
            'name': subject_name,
            'coefficient': coefficient,
            'score': score,
            'grade': grade,
            'weighted_score': weighted_score,
            'comment': comment or "No comment provided"
        }
    
    def on_ok(self):
        """Handle OK button"""
        if self.validate_data():
            self.result = True
            self.dialog.destroy()
    
    def on_cancel(self):
        """Handle Cancel button"""
        self.result = False
        self.dialog.destroy()
    
    def show(self):
        """Show the dialog and return the result"""
        self.dialog.wait_window()
        return self.result