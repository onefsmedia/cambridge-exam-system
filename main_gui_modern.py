#!/usr/bin/env python3
"""
Cambridge Report Card System with CustomTkinter - Modern UI
Beautiful, modern interface with proper button titles and clean design
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

try:
    from config import CAMBRIDGE_SUBJECTS, GRADE_THRESHOLDS, APP_SETTINGS
    from cambridge_calculator import CambridgeCalculator
    from pdf_generator import PDFGenerator
except ImportError as e:
    print(f"Import error: {e}")
    # Basic fallback settings
    APP_SETTINGS = {'title': 'Cambridge Report Card', 'version': '2.0'}
    CAMBRIDGE_SUBJECTS = {
        '0580': {'name': 'Mathematics', 'coefficient': 1.0},
        '0620': {'name': 'Chemistry', 'coefficient': 1.0},
        '0625': {'name': 'Physics', 'coefficient': 1.0},
        '0610': {'name': 'Biology', 'coefficient': 1.0},
        '0500': {'name': 'First Language English', 'coefficient': 1.0}
    }
    GRADE_THRESHOLDS = {}

class ModernCambridgeGUI:
    def __init__(self):
        # Set appearance mode and color theme
        ctk.set_appearance_mode("light")  # "light" or "dark"
        ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"
        
        # Initialize application state
        self.selected_subjects = []
        self.grades = {}
        self.subject_vars = {}
        self.grade_entries = {}
        
        try:
            self.calculator = CambridgeCalculator()
            self.pdf_generator = PDFGenerator()
        except:
            self.calculator = None
            self.pdf_generator = None
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("Cambridge International Examination - Report Card System")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Configure grid weights for responsive design
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        self.create_interface()
        
    def create_interface(self):
        """Create the modern CustomTkinter interface"""
        
        # Main container with padding
        main_frame = ctk.CTkFrame(self.root, corner_radius=15)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.grid_columnconfigure((0, 1), weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        
        # Header section - NO HIGHLIGHTING
        header_frame = ctk.CTkFrame(main_frame, corner_radius=10, fg_color="transparent")
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=(20, 10))
        
        # Title labels with no highlighting/selection
        title_label = ctk.CTkLabel(
            header_frame,
            text="Cambridge International Examination",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=("#1f538d", "#4a9eff")
        )
        title_label.pack(pady=(10, 5))
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Report Card Generator - Modern Edition",
            font=ctk.CTkFont(size=16),
            text_color=("#666666", "#cccccc")
        )
        subtitle_label.pack(pady=(0, 15))
        
        # Left column - Student Info and Subject Selection
        left_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        left_frame.grid(row=1, column=0, sticky="nsew", padx=(20, 10), pady=10)
        left_frame.grid_columnconfigure(0, weight=1)
        
        # Student Information Section
        self.create_student_info_section(left_frame)
        
        # Subject Selection Section
        self.create_subject_selection_section(left_frame)
        
        # Right column - Grades and Actions
        right_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        right_frame.grid(row=1, column=1, sticky="nsew", padx=(10, 20), pady=10)
        right_frame.grid_columnconfigure(0, weight=1)
        
        # Grade Input Section
        self.create_grade_input_section(right_frame)
        
        # Action Buttons Section
        self.create_action_buttons_section(right_frame)
        
        # Results Section
        self.create_results_section(right_frame)
    
    def create_student_info_section(self, parent):
        """Create student information section"""
        # Section title
        section_label = ctk.CTkLabel(
            parent,
            text="Student Information",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#2b2b2b", "#ffffff")
        )
        section_label.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 15))
        
        # Student Name
        name_label = ctk.CTkLabel(parent, text="Student Name:", font=ctk.CTkFont(size=14))
        name_label.grid(row=1, column=0, sticky="w", padx=20, pady=(0, 5))
        
        self.student_name_entry = ctk.CTkEntry(
            parent,
            placeholder_text="Enter student's full name",
            font=ctk.CTkFont(size=14),
            height=35
        )
        self.student_name_entry.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 15))
        
        # Candidate Number
        candidate_label = ctk.CTkLabel(parent, text="Candidate Number:", font=ctk.CTkFont(size=14))
        candidate_label.grid(row=3, column=0, sticky="w", padx=20, pady=(0, 5))
        
        self.candidate_number_entry = ctk.CTkEntry(
            parent,
            placeholder_text="Enter candidate number",
            font=ctk.CTkFont(size=14),
            height=35
        )
        self.candidate_number_entry.grid(row=4, column=0, sticky="ew", padx=20, pady=(0, 15))
        
        # School Name
        school_label = ctk.CTkLabel(parent, text="School Name:", font=ctk.CTkFont(size=14))
        school_label.grid(row=5, column=0, sticky="w", padx=20, pady=(0, 5))
        
        self.school_name_entry = ctk.CTkEntry(
            parent,
            placeholder_text="Enter school name",
            font=ctk.CTkFont(size=14),
            height=35
        )
        self.school_name_entry.grid(row=6, column=0, sticky="ew", padx=20, pady=(0, 20))
    
    def create_subject_selection_section(self, parent):
        """Create subject selection section"""
        # Section title
        section_label = ctk.CTkLabel(
            parent,
            text="Subject Selection",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#2b2b2b", "#ffffff")
        )
        section_label.grid(row=7, column=0, sticky="w", padx=20, pady=(10, 15))
        
        # Scrollable frame for subjects
        subjects_frame = ctk.CTkScrollableFrame(parent, height=200)
        subjects_frame.grid(row=8, column=0, sticky="ew", padx=20, pady=(0, 20))
        subjects_frame.grid_columnconfigure(0, weight=1)
        
        # Add subject checkboxes
        for i, (subject_code, subject_info) in enumerate(CAMBRIDGE_SUBJECTS.items()):
            var = ctk.BooleanVar()
            self.subject_vars[subject_code] = var
            
            checkbox = ctk.CTkCheckBox(
                subjects_frame,
                text=f"{subject_code}: {subject_info['name']}",
                variable=var,
                command=self.on_subject_selected,
                font=ctk.CTkFont(size=13)
            )
            checkbox.grid(row=i, column=0, sticky="w", padx=10, pady=5)
    
    def create_grade_input_section(self, parent):
        """Create grade input section"""
        # Section title
        section_label = ctk.CTkLabel(
            parent,
            text="Grade Input",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#2b2b2b", "#ffffff")
        )
        section_label.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 15))
        
        # Scrollable frame for grade inputs
        self.grades_frame = ctk.CTkScrollableFrame(parent, height=250)
        self.grades_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 20))
        self.grades_frame.grid_columnconfigure(1, weight=1)
        
        # Initial message
        self.no_subjects_label = ctk.CTkLabel(
            self.grades_frame,
            text="Select subjects above to enter grades",
            font=ctk.CTkFont(size=14),
            text_color=("#999999", "#666666")
        )
        self.no_subjects_label.grid(row=0, column=0, columnspan=2, padx=20, pady=20)
    
    def create_action_buttons_section(self, parent):
        """Create action buttons section with clear titles"""
        # Section title
        section_label = ctk.CTkLabel(
            parent,
            text="Actions",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#2b2b2b", "#ffffff")
        )
        section_label.grid(row=2, column=0, sticky="w", padx=20, pady=(10, 15))
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(parent, fg_color="transparent")
        buttons_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 20))
        buttons_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Calculate Results Button
        calculate_btn = ctk.CTkButton(
            buttons_frame,
            text="Calculate Results",
            command=self.calculate_results,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            corner_radius=8
        )
        calculate_btn.grid(row=0, column=0, sticky="ew", padx=(0, 10), pady=5)
        
        # Generate PDF Button
        pdf_btn = ctk.CTkButton(
            buttons_frame,
            text="Generate PDF Report",
            command=self.generate_pdf,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            corner_radius=8,
            fg_color=("#e74c3c", "#c0392b"),
            hover_color=("#c0392b", "#a93226")
        )
        pdf_btn.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady=5)
    
    def create_results_section(self, parent):
        """Create results display section"""
        # Section title
        section_label = ctk.CTkLabel(
            parent,
            text="Results",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#2b2b2b", "#ffffff")
        )
        section_label.grid(row=4, column=0, sticky="w", padx=20, pady=(10, 15))
        
        # Results display frame
        self.results_frame = ctk.CTkFrame(parent, corner_radius=8)
        self.results_frame.grid(row=5, column=0, sticky="ew", padx=20, pady=(0, 20))
        
        # Initial message
        self.results_label = ctk.CTkLabel(
            self.results_frame,
            text="No results yet. Enter grades and click 'Calculate Results'.",
            font=ctk.CTkFont(size=14),
            text_color=("#999999", "#666666")
        )
        self.results_label.pack(padx=20, pady=20)
    
    def on_subject_selected(self):
        """Handle subject selection changes"""
        # Get selected subjects
        self.selected_subjects = []
        for subject_code, var in self.subject_vars.items():
            if var.get():
                self.selected_subjects.append(subject_code)
        
        # Clear previous grade inputs
        for widget in self.grades_frame.winfo_children():
            widget.destroy()
        
        self.grade_entries = {}
        
        if self.selected_subjects:
            # Create grade inputs for selected subjects
            for i, subject_code in enumerate(self.selected_subjects):
                subject_name = CAMBRIDGE_SUBJECTS[subject_code]['name']
                
                # Subject label
                subject_label = ctk.CTkLabel(
                    self.grades_frame,
                    text=f"{subject_code}: {subject_name}",
                    font=ctk.CTkFont(size=13, weight="bold")
                )
                subject_label.grid(row=i, column=0, sticky="w", padx=10, pady=(10, 5))
                
                # Grade entry
                grade_entry = ctk.CTkEntry(
                    self.grades_frame,
                    placeholder_text="Grade (0-100)",
                    font=ctk.CTkFont(size=13),
                    width=120,
                    height=30
                )
                grade_entry.grid(row=i, column=1, sticky="e", padx=10, pady=(10, 5))
                
                self.grade_entries[subject_code] = grade_entry
        else:
            # Show no subjects message
            self.no_subjects_label = ctk.CTkLabel(
                self.grades_frame,
                text="Select subjects above to enter grades",
                font=ctk.CTkFont(size=14),
                text_color=("#999999", "#666666")
            )
            self.no_subjects_label.grid(row=0, column=0, columnspan=2, padx=20, pady=20)
    
    def calculate_results(self):
        """Calculate and display results"""
        if not self.selected_subjects:
            messagebox.showwarning("Warning", "Please select at least one subject.")
            return
        
        # Collect grades
        grades = {}
        try:
            for subject_code in self.selected_subjects:
                grade_text = self.grade_entries[subject_code].get().strip()
                if not grade_text:
                    messagebox.showwarning("Warning", f"Please enter a grade for {subject_code}")
                    return
                
                grade = float(grade_text)
                if not 0 <= grade <= 100:
                    messagebox.showerror("Error", f"Grade for {subject_code} must be between 0 and 100")
                    return
                
                grades[subject_code] = grade
        except ValueError:
            messagebox.showerror("Error", "All grades must be valid numbers")
            return
        
        # Calculate results
        if self.calculator:
            try:
                results = self.calculator.calculate_results(grades)
                self.display_results(results, grades)
            except Exception as e:
                messagebox.showerror("Error", f"Calculation error: {e}")
        else:
            # Simple calculation fallback
            total_score = sum(grades.values())
            average = total_score / len(grades)
            
            if average >= 90:
                overall_grade = "A*"
            elif average >= 80:
                overall_grade = "A"
            elif average >= 70:
                overall_grade = "B"
            elif average >= 60:
                overall_grade = "C"
            elif average >= 50:
                overall_grade = "D"
            else:
                overall_grade = "F"
            
            results = {
                'total_score': total_score,
                'average': average,
                'overall_grade': overall_grade
            }
            self.display_results(results, grades)
    
    def display_results(self, results, grades):
        """Display calculation results"""
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        # Results content frame
        content_frame = ctk.CTkFrame(self.results_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Overall results
        overall_label = ctk.CTkLabel(
            content_frame,
            text="Overall Results",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=("#2b2b2b", "#ffffff")
        )
        overall_label.pack(pady=(0, 10))
        
        # Results details
        details_text = f"""Total Score: {results['total_score']:.1f}
Average: {results['average']:.1f}%
Overall Grade: {results['overall_grade']}"""
        
        details_label = ctk.CTkLabel(
            content_frame,
            text=details_text,
            font=ctk.CTkFont(size=14),
            justify="left"
        )
        details_label.pack(pady=(0, 15))
        
        # Individual subject grades
        subjects_label = ctk.CTkLabel(
            content_frame,
            text="Subject Breakdown",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        subjects_label.pack(pady=(0, 5))
        
        for subject_code, grade in grades.items():
            subject_name = CAMBRIDGE_SUBJECTS[subject_code]['name']
            subject_text = f"{subject_code}: {grade}%"
            
            subject_label = ctk.CTkLabel(
                content_frame,
                text=subject_text,
                font=ctk.CTkFont(size=12)
            )
            subject_label.pack(anchor="w")
    
    def generate_pdf(self):
        """Generate PDF report"""
        student_name = self.student_name_entry.get().strip()
        candidate_number = self.candidate_number_entry.get().strip()
        school_name = self.school_name_entry.get().strip()
        
        if not student_name:
            messagebox.showwarning("Warning", "Please enter the student name.")
            return
        
        if not self.selected_subjects:
            messagebox.showwarning("Warning", "Please select subjects and enter grades.")
            return
        
        # Collect grades
        grades = {}
        try:
            for subject_code in self.selected_subjects:
                grade_text = self.grade_entries[subject_code].get().strip()
                if not grade_text:
                    messagebox.showwarning("Warning", f"Please enter a grade for {subject_code}")
                    return
                grades[subject_code] = float(grade_text)
        except ValueError:
            messagebox.showerror("Error", "All grades must be valid numbers")
            return
        
        # Generate PDF
        try:
            if self.pdf_generator:
                filename = f"{student_name.replace(' ', '_')}_report.pdf"
                self.pdf_generator.generate_report({
                    'student_name': student_name,
                    'candidate_number': candidate_number,
                    'school_name': school_name,
                    'grades': grades
                }, filename)
                messagebox.showinfo("Success", f"PDF report generated: {filename}")
            else:
                messagebox.showinfo("Info", "PDF generation not available - missing PDF generator module")
        except Exception as e:
            messagebox.showerror("Error", f"PDF generation failed: {e}")
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

def main():
    """Main entry point"""
    try:
        app = ModernCambridgeGUI()
        app.run()
    except Exception as e:
        print(f"Application error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()