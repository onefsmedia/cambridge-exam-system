#!/usr/bin/env python3
"""
Cambridge Report Card System - Complete Modern Version
Features: Auto-generated candidate numbers, teacher comments, coefficient modification,
dynamic grading, comprehensive PDF generation, complete Cambridge subjects
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
import sys
from pathlib import Path
import random
from datetime import datetime
import os
import subprocess
import platform
import webbrowser
import urllib.parse

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

try:
    from config import CAMBRIDGE_SUBJECTS, GRADE_THRESHOLDS, APP_SETTINGS
    from cambridge_calculator import CambridgeCalculator
    from pdf_generator import CambridgePDFGenerator as PDFGenerator
except ImportError as e:
    print(f"Import error: {e}")
    # Will work with what we have

class ComprehensiveCambridgeGUI:
    def __init__(self):
        # Set appearance mode and color theme
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Initialize application state
        self.selected_subjects = []
        self.grades = {}
        self.comments = {}
        self.coefficients = {}
        self.subject_vars = {}
        self.grade_entries = {}
        self.comment_entries = {}
        self.coefficient_entries = {}
        self.grade_labels = {}  # For dynamic grade display
        
        try:
            self.calculator = CambridgeCalculator()
            self.pdf_generator = PDFGenerator()
        except:
            self.calculator = None
            self.pdf_generator = None
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("Cambridge International Examination - Report Card System")
        self.root.geometry("1600x1000")
        self.root.minsize(1400, 900)
        
        # Configure grid weights for responsive design
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Load coefficients from config
        self.load_default_coefficients()
        
        self.create_interface()
        
    def load_default_coefficients(self):
        """Load default coefficients from config"""
        for subject_code, subject_info in CAMBRIDGE_SUBJECTS.items():
            self.coefficients[subject_code] = subject_info['coefficient']
    
    def generate_candidate_number(self):
        """Generate auto candidate number"""
        # Format: Year + Random 4-digit number
        year = datetime.now().year
        random_num = random.randint(1000, 9999)
        return f"{year}{random_num}"
    
    def wrap_text(self, text, max_length=16):
        """Wrap text to fit within specified length, optimized for UI display"""
        if len(text) <= max_length:
            return text
        
        # For very long subject names, use more aggressive wrapping
        if len(text) > 25:  # Very long names need special handling
            max_length = 12  # Use shorter lines for very long text
        
        # Find a good break point
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            # Check if adding this word would exceed the limit
            test_line = current_line + (" " + word if current_line else word)
            
            if len(test_line) <= max_length:
                current_line = test_line
            else:
                # If current line has content, save it and start new line
                if current_line:
                    lines.append(current_line)
                    current_line = word
                    # If the single word is still too long, break it up
                    if len(current_line) > max_length:
                        lines.append(current_line[:max_length-3] + "...")
                        current_line = ""
                else:
                    # Word itself is too long, truncate it
                    lines.append(word[:max_length-3] + "...")
                    current_line = ""
        
        if current_line:
            lines.append(current_line)
        
        return "\n".join(lines)
    
    def calculate_grade_from_score(self, score):
        """Calculate letter grade from numerical score"""
        try:
            score = float(score)
            if score >= 90:
                return 'A*'
            elif score >= 80:
                return 'A'
            elif score >= 70:
                return 'B'
            elif score >= 60:
                return 'C'
            elif score >= 50:
                return 'D'
            elif score >= 40:
                return 'E'
            elif score >= 30:
                return 'F'
            elif score >= 20:
                return 'G'
            else:
                return 'U'
        except:
            return '-'
    
    def create_interface(self):
        """Create the comprehensive CustomTkinter interface with student info at top"""
        
        # Main container with padding
        main_frame = ctk.CTkFrame(self.root, corner_radius=15)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=0)  # Header - fixed height
        main_frame.grid_rowconfigure(1, weight=0)  # Student info - fixed height
        main_frame.grid_rowconfigure(2, weight=1)  # Main content - expandable
        
        # Header section
        header_frame = ctk.CTkFrame(main_frame, corner_radius=10, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        
        # Title labels
        title_label = ctk.CTkLabel(
            header_frame,
            text="Cambridge International Examination",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=("#1f538d", "#4a9eff")
        )
        title_label.pack(pady=(10, 5))
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Complete Report Card Generator - Professional Edition",
            font=ctk.CTkFont(size=16),
            text_color=("#666666", "#cccccc")
        )
        subtitle_label.pack(pady=(0, 15))
        
        # Student Information section spanning full width
        student_frame = ctk.CTkFrame(main_frame, corner_radius=10, border_width=2, border_color=("#1f538d", "#4a9eff"))
        student_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))
        student_frame.grid_columnconfigure(0, weight=1)
        student_frame.grid_columnconfigure(1, weight=1)
        student_frame.grid_columnconfigure(2, weight=1)
        student_frame.grid_columnconfigure(3, weight=1)
        
        # Main content area with two columns - adjusted for better balance
        content_frame = ctk.CTkFrame(main_frame, corner_radius=10, fg_color="transparent")
        content_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
        content_frame.grid_columnconfigure(0, weight=3)  # Left column gets more space for grading
        content_frame.grid_columnconfigure(1, weight=2)  # Right column for results
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Left column - Subject Selection and Grading
        left_frame = ctk.CTkFrame(content_frame, corner_radius=10)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=0)
        left_frame.grid_columnconfigure(0, weight=1)
        left_frame.grid_rowconfigure(0, weight=0)  # Title - fixed
        left_frame.grid_rowconfigure(1, weight=0)  # Search label - fixed
        left_frame.grid_rowconfigure(2, weight=0)  # Search entry - fixed
        left_frame.grid_rowconfigure(3, weight=1)  # Subjects frame - expandable
        left_frame.grid_rowconfigure(4, weight=1)  # Grading frame - expandable
        
        # Right column - Actions and Results
        right_frame = ctk.CTkFrame(content_frame, corner_radius=10)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=0)
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_rowconfigure(0, weight=0)  # Title - fixed
        right_frame.grid_rowconfigure(1, weight=0)  # Calculate button - fixed
        right_frame.grid_rowconfigure(2, weight=0)  # PDF button - fixed
        right_frame.grid_rowconfigure(3, weight=0)  # Email button - fixed
        right_frame.grid_rowconfigure(4, weight=0)  # Results label - fixed
        right_frame.grid_rowconfigure(5, weight=1)  # Results area - expandable
        
        # Create sections
        self.create_student_info_section(student_frame)
        self.create_subject_grading_section(left_frame)
        self.create_actions_results_section(right_frame)
    
    def create_student_info_section(self, parent):
        """Create comprehensive student information section - horizontal layout"""
        # Section title spanning full width
        section_label = ctk.CTkLabel(
            parent,
            text="📋 Student Information",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=("#1f538d", "#4a9eff")
        )
        section_label.grid(row=0, column=0, columnspan=4, sticky="w", padx=20, pady=(20, 15))
        
        # First column - Student Name
        name_label = ctk.CTkLabel(parent, text="Student Name:", font=ctk.CTkFont(size=14))
        name_label.grid(row=1, column=0, sticky="w", padx=(20, 10), pady=(0, 5))
        
        self.student_name_entry = ctk.CTkEntry(
            parent,
            placeholder_text="Enter student's full name",
            font=ctk.CTkFont(size=14),
            height=35
        )
        self.student_name_entry.grid(row=2, column=0, sticky="ew", padx=(20, 10), pady=(0, 15))
        
        # Second column - Candidate Number
        candidate_label = ctk.CTkLabel(parent, text="Candidate Number:", font=ctk.CTkFont(size=14))
        candidate_label.grid(row=1, column=1, sticky="w", padx=10, pady=(0, 5))
        
        candidate_input_frame = ctk.CTkFrame(parent, fg_color="transparent")
        candidate_input_frame.grid(row=2, column=1, sticky="ew", padx=10, pady=(0, 15))
        candidate_input_frame.grid_columnconfigure(0, weight=1)
        
        self.candidate_number_entry = ctk.CTkEntry(
            candidate_input_frame,
            placeholder_text="Auto-generated",
            font=ctk.CTkFont(size=14),
            height=35
        )
        self.candidate_number_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        auto_generate_btn = ctk.CTkButton(
            candidate_input_frame,
            text="Generate",
            command=self.auto_generate_candidate_number,
            font=ctk.CTkFont(size=12),
            height=35,
            width=80
        )
        auto_generate_btn.grid(row=0, column=1, sticky="e")
        
        # Third column - School Name
        school_label = ctk.CTkLabel(parent, text="School Name:", font=ctk.CTkFont(size=14))
        school_label.grid(row=1, column=2, sticky="w", padx=10, pady=(0, 5))
        
        self.school_name_entry = ctk.CTkEntry(
            parent,
            placeholder_text="Enter school name",
            font=ctk.CTkFont(size=14),
            height=35
        )
        self.school_name_entry.grid(row=2, column=2, sticky="ew", padx=10, pady=(0, 15))
        
        # Fourth column - Examination Session
        session_label = ctk.CTkLabel(parent, text="Examination Session:", font=ctk.CTkFont(size=14))
        session_label.grid(row=1, column=3, sticky="w", padx=(10, 20), pady=(0, 5))
        
        self.session_combo = ctk.CTkComboBox(
            parent,
            values=APP_SETTINGS.get('examination_sessions', ['May/June 2025']),
            font=ctk.CTkFont(size=14),
            height=35
        )
        self.session_combo.grid(row=2, column=3, sticky="ew", padx=(10, 20), pady=(0, 15))
        self.session_combo.set("May/June 2025")  # Default value
        
        # Auto-generate candidate number on startup
        self.auto_generate_candidate_number()
    
    def auto_generate_candidate_number(self):
        """Auto-generate candidate number"""
        candidate_number = self.generate_candidate_number()
        self.candidate_number_entry.delete(0, tk.END)
        self.candidate_number_entry.insert(0, candidate_number)
    
    def create_subject_grading_section(self, parent):
        """Create combined subject selection and grading section"""
        # Section title
        section_label = ctk.CTkLabel(
            parent,
            text="📚 Subject Selection & Grading",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#1f538d", "#4a9eff")
        )
        section_label.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 15))
        
        # Subject selection with search
        search_label = ctk.CTkLabel(parent, text="Search Subjects:", font=ctk.CTkFont(size=14))
        search_label.grid(row=1, column=0, sticky="w", padx=20, pady=(0, 5))
        
        self.search_entry = ctk.CTkEntry(
            parent,
            placeholder_text="Type to search subjects...",
            font=ctk.CTkFont(size=12),
            height=30
        )
        self.search_entry.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 10))
        self.search_entry.bind("<KeyRelease>", self.filter_subjects)
        
        # Scrollable frame for subjects - reduced height for better fit
        self.subjects_frame = ctk.CTkScrollableFrame(parent, height=250, label_text="Available Subjects")
        self.subjects_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=(0, 10))
        self.subjects_frame.grid_columnconfigure(0, weight=1)
        
        # Create subject checkboxes
        self.create_subject_checkboxes()
        
        # Selected subjects grading area - reduced height for better fit
        self.grading_frame = ctk.CTkScrollableFrame(parent, height=150, label_text="Grade Input & Comments")
        self.grading_frame.grid(row=4, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.grading_frame.grid_columnconfigure(0, weight=0, minsize=170)  # Subject - increased width
        self.grading_frame.grid_columnconfigure(1, weight=0, minsize=80)   # Score - fixed width
        self.grading_frame.grid_columnconfigure(2, weight=0, minsize=60)   # Grade - fixed width
        self.grading_frame.grid_columnconfigure(3, weight=0, minsize=70)   # Coeff - reduced width
        self.grading_frame.grid_columnconfigure(4, weight=1, minsize=250)  # Comments - expandable
        
        # Show initial headers and sample data for demonstration
        self.show_grading_headers()
    
    def show_grading_headers(self):
        """Show the grading headers initially"""
        # Clear any existing content
        for widget in self.grading_frame.winfo_children():
            widget.destroy()
        
        # Create headers
        headers = ["Subject", "Score", "Grade", "Coeff", "Teacher Comments"]
        header_widths = [170, 80, 60, 70, 250]  # Adjusted widths - moved 20px from Coeff to Subject
        
        for i, (header, width) in enumerate(zip(headers, header_widths)):
            header_label = ctk.CTkLabel(
                self.grading_frame,
                text=header,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=("#1f538d", "#4a9eff"),
                width=width
            )
            header_label.grid(row=0, column=i, padx=5, pady=10, sticky="w" if i == 0 else "ew")
        
        # Show instructional message
        instruction_label = ctk.CTkLabel(
            self.grading_frame,
            text="👆 Select subjects above to start grading",
            font=ctk.CTkFont(size=12),
            text_color=("#999999", "#666666")
        )
        instruction_label.grid(row=1, column=0, columnspan=5, padx=20, pady=15)
    
    def create_subject_checkboxes(self):
        """Create checkboxes for all Cambridge subjects"""
        for i, (subject_code, subject_info) in enumerate(CAMBRIDGE_SUBJECTS.items()):
            var = ctk.BooleanVar()
            self.subject_vars[subject_code] = var
            
            # Subject frame
            subject_frame = ctk.CTkFrame(self.subjects_frame, fg_color="transparent")
            subject_frame.grid(row=i, column=0, sticky="ew", padx=5, pady=2)
            subject_frame.grid_columnconfigure(0, weight=1)
            
            checkbox = ctk.CTkCheckBox(
                subject_frame,
                text=f"{subject_code}: {subject_info['name']}",
                variable=var,
                command=self.on_subject_selected,
                font=ctk.CTkFont(size=12)
            )
            checkbox.grid(row=0, column=0, sticky="w", padx=5, pady=2)
    
    def filter_subjects(self, event=None):
        """Filter subjects based on search term"""
        search_term = self.search_entry.get().lower()
        
        # Clear current subjects
        for widget in self.subjects_frame.winfo_children():
            widget.destroy()
        
        # Show filtered subjects
        row = 0
        for subject_code, subject_info in CAMBRIDGE_SUBJECTS.items():
            subject_text = f"{subject_code}: {subject_info['name']}".lower()
            
            if search_term in subject_text:
                subject_frame = ctk.CTkFrame(self.subjects_frame, fg_color="transparent")
                subject_frame.grid(row=row, column=0, sticky="ew", padx=5, pady=2)
                subject_frame.grid_columnconfigure(0, weight=1)
                
                checkbox = ctk.CTkCheckBox(
                    subject_frame,
                    text=f"{subject_code}: {subject_info['name']}",
                    variable=self.subject_vars[subject_code],
                    command=self.on_subject_selected,
                    font=ctk.CTkFont(size=12)
                )
                checkbox.grid(row=0, column=0, sticky="w", padx=5, pady=2)
                row += 1
    
    def on_subject_selected(self):
        """Handle subject selection changes"""
        # Get selected subjects
        self.selected_subjects = []
        for subject_code, var in self.subject_vars.items():
            if var.get():
                self.selected_subjects.append(subject_code)
        
        # Clear previous grading inputs
        for widget in self.grading_frame.winfo_children():
            widget.destroy()
        
        self.grade_entries = {}
        self.comment_entries = {}
        self.coefficient_entries = {}
        self.grade_labels = {}
        
        if self.selected_subjects:
            # Create headers
            headers = ["Subject", "Score", "Grade", "Coeff", "Teacher Comments"]
            header_widths = [170, 80, 60, 70, 250]  # Adjusted widths - moved 20px from Coeff to Subject
            
            for i, (header, width) in enumerate(zip(headers, header_widths)):
                header_label = ctk.CTkLabel(
                    self.grading_frame,
                    text=header,
                    font=ctk.CTkFont(size=13, weight="bold"),
                    text_color=("#1f538d", "#4a9eff"),
                    width=width
                )
                header_label.grid(row=0, column=i, padx=5, pady=5, sticky="w" if i == 0 else "ew")
            
            # Create grading inputs for selected subjects
            for i, subject_code in enumerate(self.selected_subjects, 1):
                subject_name = CAMBRIDGE_SUBJECTS[subject_code]['name']
                
                # Subject label - let CustomTkinter handle wrapping automatically
                subject_display = f"{subject_code}: {subject_name}"
                
                subject_label = ctk.CTkLabel(
                    self.grading_frame,
                    text=subject_display,
                    font=ctk.CTkFont(size=10),
                    justify="left",
                    width=170,  # Increased width from 150 to 170
                    height=60,  # Increased height for multi-line text
                    anchor="nw",  # Align to top-left
                    wraplength=160  # Increased wraplength from 140 to 160
                )
                subject_label.grid(row=i, column=0, padx=5, pady=5, sticky="nw")
                
                # Score entry
                score_entry = ctk.CTkEntry(
                    self.grading_frame,
                    placeholder_text="0-100",
                    font=ctk.CTkFont(size=12),
                    width=80,
                    height=30
                )
                score_entry.grid(row=i, column=1, padx=5, pady=5)
                # Bind both key release and focus out events for immediate grade calculation
                score_entry.bind("<KeyRelease>", lambda e, sc=subject_code: self.update_dynamic_grade(sc))
                score_entry.bind("<FocusOut>", lambda e, sc=subject_code: self.update_dynamic_grade(sc))
                self.grade_entries[subject_code] = score_entry
                
                # Grade display (dynamic)
                grade_label = ctk.CTkLabel(
                    self.grading_frame,
                    text="-",
                    font=ctk.CTkFont(size=12, weight="bold"),
                    width=60
                )
                grade_label.grid(row=i, column=2, padx=5, pady=5)
                self.grade_labels[subject_code] = grade_label
                
                # Coefficient entry
                coeff_entry = ctk.CTkEntry(
                    self.grading_frame,
                    font=ctk.CTkFont(size=12),
                    width=70,  # Reduced from 90 to 70
                    height=30
                )
                coeff_entry.insert(0, str(self.coefficients.get(subject_code, 1.0)))
                coeff_entry.grid(row=i, column=3, padx=5, pady=5)
                self.coefficient_entries[subject_code] = coeff_entry
                
                # Teacher comment entry (multiline text box)
                comment_entry = ctk.CTkTextbox(
                    self.grading_frame,
                    font=ctk.CTkFont(size=11),
                    width=250,
                    height=60
                )
                comment_entry.insert("0.0", "Enter detailed teacher comments...")
                comment_entry.grid(row=i, column=4, padx=5, pady=5, sticky="ew")
                self.comment_entries[subject_code] = comment_entry
        else:
            # Show headers and instruction when no subjects are selected
            self.show_grading_headers()
    
    def update_dynamic_grade(self, subject_code):
        """Update grade dynamically as score is entered"""
        try:
            score_text = self.grade_entries[subject_code].get().strip()
            if score_text and score_text.replace('.', '').isdigit():
                score = float(score_text)
                # Validate score range
                if 0 <= score <= 100:
                    grade = self.calculate_grade_from_score(score)
                    self.grade_labels[subject_code].configure(text=grade)
                    
                    # Color coding for grades
                    if grade in ['A*', 'A']:
                        color = "#2ecc71"  # Green
                    elif grade in ['B', 'C']:
                        color = "#f39c12"  # Orange
                    elif grade in ['D', 'E']:
                        color = "#e67e22"  # Orange-red
                    else:
                        color = "#e74c3c"  # Red
                    
                    self.grade_labels[subject_code].configure(text_color=color)
                else:
                    # Score out of range
                    self.grade_labels[subject_code].configure(text="Invalid", text_color="#e74c3c")
            else:
                self.grade_labels[subject_code].configure(text="-", text_color=("#666666", "#cccccc"))
        except (ValueError, AttributeError):
            self.grade_labels[subject_code].configure(text="-", text_color=("#666666", "#cccccc"))
    
    def create_actions_results_section(self, parent):
        """Create actions and results section"""
        # Section title
        section_label = ctk.CTkLabel(
            parent,
            text="⚙️ Actions & Results",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#1f538d", "#4a9eff")
        )
        section_label.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 15))
        
        # Action buttons
        calculate_btn = ctk.CTkButton(
            parent,
            text="Calculate Results",
            command=self.calculate_comprehensive_results,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            corner_radius=8
        )
        calculate_btn.grid(row=1, column=0, sticky="ew", padx=20, pady=5)
        
        pdf_btn = ctk.CTkButton(
            parent,
            text="Generate PDF Report",
            command=self.generate_comprehensive_pdf,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            corner_radius=8,
            fg_color=("#1f2937", "#1f538d"),
            hover_color=("#374151", "#4a9eff")
        )
        pdf_btn.grid(row=2, column=0, sticky="ew", padx=20, pady=5)
        
        # Email button
        email_btn = ctk.CTkButton(
            parent,
            text="📧 Email Report",
            command=self.email_report,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            corner_radius=8,
            fg_color=("#059669", "#10b981"),
            hover_color=("#047857", "#34d399")
        )
        email_btn.grid(row=3, column=0, sticky="ew", padx=20, pady=5)
        
        # Results section
        results_label = ctk.CTkLabel(
            parent,
            text="Report Card Preview",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=("#2b2b2b", "#ffffff")
        )
        results_label.grid(row=4, column=0, sticky="w", padx=20, pady=(20, 10))
        
        # Results display frame - reduced height for better fit
        self.results_frame = ctk.CTkScrollableFrame(parent, height=300)
        self.results_frame.grid(row=5, column=0, sticky="nsew", padx=20, pady=(0, 20))
        
        # Initial message
        self.results_text = ctk.CTkTextbox(
            self.results_frame,
            font=ctk.CTkFont(size=12),
            height=300
        )
        self.results_text.pack(fill="both", expand=True, padx=10, pady=10)
        self.results_text.insert("0.0", "Enter student information and grades, then click 'Calculate Results' to see the report card preview here.")
    
    def calculate_comprehensive_results(self):
        """Calculate comprehensive results with report card format"""
        if not self.selected_subjects:
            messagebox.showwarning("Warning", "Please select at least one subject.")
            return
        
        # Collect data
        student_name = self.student_name_entry.get().strip()
        candidate_number = self.candidate_number_entry.get().strip()
        school_name = self.school_name_entry.get().strip()
        session = self.session_combo.get()
        
        if not student_name:
            messagebox.showwarning("Warning", "Please enter student name.")
            return
        
        # Collect grades, coefficients, and comments
        grades_data = {}
        comments = {}
        
        try:
            for subject_code in self.selected_subjects:
                score_text = self.grade_entries[subject_code].get().strip()
                coeff_text = self.coefficient_entries[subject_code].get().strip()
                comment = self.comment_entries[subject_code].get("0.0", tk.END).strip()
                
                if not score_text:
                    messagebox.showwarning("Warning", f"Please enter a score for {subject_code}")
                    return
                
                score = float(score_text)
                coefficient = float(coeff_text) if coeff_text else 1.0
                
                if not 0 <= score <= 100:
                    messagebox.showerror("Error", f"Score for {subject_code} must be between 0 and 100")
                    return
                
                grades_data[subject_code] = {
                    'score': score,
                    'coefficient': coefficient
                }
                comments[subject_code] = comment if comment else "Good effort"
                
        except ValueError as e:
            messagebox.showerror("Error", "All scores and coefficients must be valid numbers")
            return
        
        # Calculate results using calculator
        if self.calculator:
            results = self.calculator.calculate_results(grades_data)
        else:
            # Fallback calculation
            total_weighted = sum(data['score'] * data['coefficient'] for data in grades_data.values())
            total_coeffs = sum(data['coefficient'] for data in grades_data.values())
            avg = total_weighted / total_coeffs if total_coeffs > 0 else 0
            
            results = {
                'subject_results': {code: {
                    'score': data['score'],
                    'grade': self.calculate_grade_from_score(data['score']),
                    'coefficient': data['coefficient']
                } for code, data in grades_data.items()},
                'overall_average': avg,
                'overall_grade': self.calculate_grade_from_score(avg),
                'total_subjects': len(grades_data)
            }
        
        # Display comprehensive report card preview
        self.display_report_card_preview(student_name, candidate_number, school_name, session, results, comments)
    
    def display_report_card_preview(self, student_name, candidate_number, school_name, session, results, comments):
        """Display report card preview in exact format"""
        self.results_text.delete("0.0", tk.END)
        
        # Header
        report = "═" * 60 + "\n"
        report += "   CAMBRIDGE INTERNATIONAL EXAMINATION\n"
        report += "        General Certificate of Education\n"
        report += "═" * 60 + "\n\n"
        
        # Student Information
        report += "STUDENT INFORMATION:\n"
        report += "─" * 30 + "\n"
        report += f"Name: {student_name}\n"
        report += f"Candidate Number: {candidate_number}\n"
        report += f"School: {school_name}\n"
        report += f"Session: {session}\n"
        report += f"Date of Issue: {datetime.now().strftime('%B %d, %Y')}\n\n"
        
        # Results Table
        report += "EXAMINATION RESULTS:\n"
        report += "─" * 75 + "\n"
        report += f"{'Subject Code':<12} {'Subject Name':<25} {'Score':<8} {'Grade':<6} {'Comments':<20}\n"
        report += "─" * 75 + "\n"
        
        for subject_code in self.selected_subjects:
            subject_name = CAMBRIDGE_SUBJECTS[subject_code]['name']
            subject_result = results['subject_results'][subject_code]
            comment = comments.get(subject_code, 'Good effort')
            
            # Truncate long names and comments
            short_name = subject_name[:24] if len(subject_name) > 24 else subject_name
            short_comment = comment[:19] if len(comment) > 19 else comment
            
            report += f"{subject_code:<12} {short_name:<25} {subject_result['score']:<8.0f} {subject_result['grade']:<6} {short_comment:<20}\n"
        
        report += "─" * 75 + "\n\n"
        
        # Overall Performance
        report += "OVERALL PERFORMANCE:\n"
        report += "─" * 25 + "\n"
        report += f"Total Subjects: {results['total_subjects']}\n"
        report += f"Overall Average: {results['overall_average']:.1f}%\n"
        report += f"Overall Grade: {results['overall_grade']}\n\n"
        
        # Grade Scale
        report += "GRADE SCALE:\n"
        report += "─" * 15 + "\n"
        report += "A* = 90-100%    A = 80-89%     B = 70-79%\n"
        report += "C = 60-69%      D = 50-59%     E = 40-49%\n"
        report += "F = 30-39%      G = 20-29%     U = Below 20%\n\n"
        
        # Footer
        report += "─" * 60 + "\n"
        report += "This is an official Cambridge International result.\n"
        report += "Issued by Cambridge Assessment International Education\n"
        report += "─" * 60 + "\n"
        
        self.results_text.insert("0.0", report)
    
    def generate_comprehensive_pdf(self):
        """Generate comprehensive PDF report"""
        if not self.selected_subjects:
            messagebox.showwarning("Warning", "Please calculate results first.")
            return
        
        student_name = self.student_name_entry.get().strip()
        if not student_name:
            messagebox.showwarning("Warning", "Please enter student name.")
            return
        
        # Calculate totals for final grade summary
        total_weighted_score = 0
        total_coefficient = 0
        subjects_data = []
        
        # Collect grades and comments and calculate totals
        for subject_code in self.selected_subjects:
            try:
                # Get raw score
                score = float(self.grade_entries[subject_code].get().strip())
                
                # Get coefficient for this subject
                coefficient = CAMBRIDGE_SUBJECTS[subject_code]['coefficient']
                
                # Calculate grade and weighted score
                grade = self.calculate_grade_from_score(score)
                weighted_score = score * coefficient
                
                # Get comment
                comment = self.comment_entries[subject_code].get("0.0", tk.END).strip()
                if not comment or comment == "Enter detailed teacher comments...":
                    comment = "Good effort"
                
                # Add to totals
                total_weighted_score += weighted_score
                total_coefficient += coefficient
                
                # Create subject data structure expected by PDF generator
                subject_data = {
                    'name': CAMBRIDGE_SUBJECTS[subject_code]['name'],
                    'coefficient': coefficient,
                    'score': score,
                    'grade': grade,
                    'weighted_score': round(weighted_score, 2),
                    'comment': comment
                }
                subjects_data.append(subject_data)
                
            except ValueError:
                # Skip subjects with invalid scores
                continue
        
        # Calculate final grade
        if total_coefficient > 0:
            weighted_average = total_weighted_score / total_coefficient
            final_grade = self.calculate_grade_from_score(weighted_average)
        else:
            weighted_average = 0
            final_grade = "N/A"
        
        # Prepare student data in the format expected by PDF generator
        student_data = {
            'name': student_name,  # PDF generator expects 'name', not 'student_name'
            'candidate_number': self.candidate_number_entry.get().strip(),
            'school': self.school_name_entry.get().strip(),
            'exam_session': self.session_combo.get(),
            'subjects': subjects_data,  # PDF generator expects 'subjects' array
            'final_grade': {
                'total_weighted_score': round(total_weighted_score, 2),
                'total_coefficient': total_coefficient,
                'weighted_average': round(weighted_average, 2),
                'final_grade': final_grade
            }
        }
        
        # Generate PDF
        try:
            if self.pdf_generator:
                filename = f"{student_name.replace(' ', '_')}_cambridge_report.pdf"
                pdf_path = self.pdf_generator.generate_report(student_data, filename)
                
                # Show success message with options
                result = messagebox.askyesno(
                    "PDF Generated Successfully!", 
                    f"PDF report generated successfully!\nFile: {pdf_path}\n\nWould you like to open the PDF now?",
                    icon="question"
                )
                
                if result:
                    self.open_pdf_in_system(pdf_path)
                    
                # Store the last generated PDF path for email functionality
                self.last_generated_pdf = pdf_path
                
            else:
                messagebox.showerror("Error", "PDF generation module not available. Please check if reportlab is installed.\nRun: pip install reportlab")
        except Exception as e:
            messagebox.showerror("Error", f"PDF generation failed: {str(e)}\n\nTry installing reportlab: pip install reportlab")
    
    def open_pdf_in_system(self, pdf_path):
        """Open PDF file in the system's default PDF reader"""
        try:
            system = platform.system()
            if system == "Windows":
                os.startfile(pdf_path)
            elif system == "Darwin":  # macOS
                subprocess.run(["open", pdf_path])
            else:  # Linux and other Unix-like systems
                subprocess.run(["xdg-open", pdf_path])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open PDF: {str(e)}")
    
    def email_report(self):
        """Email the generated PDF report"""
        # Check if a PDF has been generated
        if not hasattr(self, 'last_generated_pdf') or not self.last_generated_pdf:
            response = messagebox.askyesno(
                "No PDF Generated", 
                "No PDF report has been generated yet.\n\nWould you like to generate one first?",
                icon="question"
            )
            if response:
                self.generate_comprehensive_pdf()
                return
            else:
                return
        
        # Check if the PDF file still exists
        if not os.path.exists(self.last_generated_pdf):
            messagebox.showerror("Error", "The PDF file no longer exists. Please generate a new report.")
            return
        
        # Get student name for email subject
        student_name = self.student_name_entry.get().strip() or "Student"
        
        # Create email dialog
        self.show_email_dialog(student_name)
    
    def show_email_dialog(self, student_name):
        """Show email composition dialog"""
        # Create email dialog window
        email_dialog = ctk.CTkToplevel(self.root)
        email_dialog.title("Email Report")
        email_dialog.geometry("600x500")
        email_dialog.transient(self.root)
        email_dialog.grab_set()
        
        # Center the dialog
        email_dialog.update_idletasks()
        x = (email_dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (email_dialog.winfo_screenheight() // 2) - (500 // 2)
        email_dialog.geometry(f"600x500+{x}+{y}")
        
        # Configure grid
        email_dialog.grid_columnconfigure(0, weight=1)
        email_dialog.grid_rowconfigure(3, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(
            email_dialog,
            text="📧 Email Cambridge Report",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=("#1f538d", "#4a9eff")
        )
        title_label.grid(row=0, column=0, padx=20, pady=(20, 15), sticky="w")
        
        # Recipient email
        email_label = ctk.CTkLabel(email_dialog, text="Recipient Email:", font=ctk.CTkFont(size=14))
        email_label.grid(row=1, column=0, padx=20, pady=(0, 5), sticky="w")
        
        email_entry = ctk.CTkEntry(
            email_dialog,
            placeholder_text="Enter recipient's email address",
            font=ctk.CTkFont(size=12),
            height=35
        )
        email_entry.grid(row=2, column=0, padx=20, pady=(0, 15), sticky="ew")
        
        # Email content
        content_label = ctk.CTkLabel(email_dialog, text="Email Message:", font=ctk.CTkFont(size=14))
        content_label.grid(row=3, column=0, padx=20, pady=(0, 5), sticky="nw")
        
        # Pre-filled email content
        default_message = f"""Dear Recipient,

Please find attached the Cambridge International Examination report card for {student_name}.

This report contains:
- Detailed subject grades and performance
- Teacher comments for each subject
- Overall academic summary

Best regards,
Cambridge Report System
"""
        
        content_text = ctk.CTkTextbox(
            email_dialog,
            font=ctk.CTkFont(size=12),
            height=200
        )
        content_text.grid(row=4, column=0, padx=20, pady=(0, 15), sticky="nsew")
        content_text.insert("0.0", default_message)
        
        # Buttons frame
        button_frame = ctk.CTkFrame(email_dialog, fg_color="transparent")
        button_frame.grid(row=5, column=0, padx=20, pady=(0, 20), sticky="ew")
        button_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Cancel button
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=email_dialog.destroy,
            font=ctk.CTkFont(size=14),
            height=40,
            fg_color=("#6b7280", "#9ca3af"),
            hover_color=("#4b5563", "#6b7280")
        )
        cancel_btn.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        
        # Send button
        send_btn = ctk.CTkButton(
            button_frame,
            text="Send Email",
            command=lambda: self.send_email(
                email_entry.get().strip(),
                f"Cambridge Report Card - {student_name}",
                content_text.get("0.0", tk.END).strip(),
                email_dialog
            ),
            font=ctk.CTkFont(size=14),
            height=40,
            fg_color=("#059669", "#10b981"),
            hover_color=("#047857", "#34d399")
        )
        send_btn.grid(row=0, column=1, padx=(10, 0), sticky="ew")
    
    def send_email(self, recipient, subject, body, dialog):
        """Send email using the system's default email client"""
        try:
            if not recipient:
                messagebox.showerror("Error", "Please enter a recipient email address.")
                return
            
            # Basic email validation
            if "@" not in recipient or "." not in recipient.split("@")[-1]:
                messagebox.showerror("Error", "Please enter a valid email address.")
                return
            
            # Prepare email parameters
            subject_encoded = urllib.parse.quote(subject)
            body_encoded = urllib.parse.quote(body)
            
            # Create mailto URL
            mailto_url = f"mailto:{recipient}?subject={subject_encoded}&body={body_encoded}"
            
            # Add attachment note to body (most email clients don't support direct attachment via mailto)
            attachment_note = f"\n\n[NOTE: Please attach the PDF file: {os.path.basename(self.last_generated_pdf)}]"
            body_with_note = body + attachment_note
            body_encoded_with_note = urllib.parse.quote(body_with_note)
            
            mailto_url_with_note = f"mailto:{recipient}?subject={subject_encoded}&body={body_encoded_with_note}"
            
            # Try to open the email client
            webbrowser.open(mailto_url_with_note)
            
            # Show success message with instructions
            dialog.destroy()
            messagebox.showinfo(
                "Email Client Opened",
                f"Your default email client has been opened with:\n"
                f"• Recipient: {recipient}\n"
                f"• Subject: {subject}\n"
                f"• Pre-filled message\n\n"
                f"Please manually attach the PDF file:\n{self.last_generated_pdf}\n\n"
                f"The PDF location has been copied to your clipboard if possible."
            )
            
            # Try to copy PDF path to clipboard
            try:
                self.root.clipboard_clear()
                self.root.clipboard_append(self.last_generated_pdf)
            except:
                pass  # Clipboard operation failed, but email can still be sent manually
                
        except Exception as e:
            messagebox.showerror("Error", f"Could not open email client: {str(e)}\n\nPlease manually email the PDF file located at:\n{self.last_generated_pdf}")
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

def main():
    """Main entry point"""
    try:
        app = ComprehensiveCambridgeGUI()
        app.run()
    except Exception as e:
        print(f"Application error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()