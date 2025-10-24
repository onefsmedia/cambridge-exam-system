#!/usr/bin/env python3
"""
Simplified Cambridge Report Card System with Dear PyGui - Fixed Version
"""

import dearpygui.dearpygui as dpg
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
    print("Some features may not work properly")
    # Basic fallback settings
    APP_SETTINGS = {'title': 'Cambridge Report Card', 'version': '2.0'}
    CAMBRIDGE_SUBJECTS = {}
    GRADE_THRESHOLDS = {}

class CambridgeReportGUI:
    def __init__(self):
        # Initialize application state
        self.selected_subjects = []
        self.grades = {}
        self.calculator = None
        self.pdf_generator = None
        
        try:
            self.calculator = CambridgeCalculator()
            self.pdf_generator = PDFGenerator()
        except:
            pass
        
        # Initialize Dear PyGui
        dpg.create_context()
        
        # Create a simple viewport that should work
        dpg.create_viewport(
            title="Cambridge Report Card System",
            width=1200,
            height=800,
            resizable=True
        )
        
        # Create the main window
        self.create_main_window()
        
        # Setup and run
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("main_window", True)
        dpg.start_dearpygui()
        dpg.destroy_context()
    
    def create_main_window(self):
        """Create the main application window"""
        with dpg.window(label="Cambridge Report Card System", tag="main_window"):
            # Header
            dpg.add_text("Cambridge International Examination", color=(0, 0, 0, 255))
            dpg.add_text("Report Card Generator", color=(0, 0, 0, 255))
            dpg.add_separator()
            dpg.add_spacer(height=20)
            
            # Student Information Section
            dpg.add_text("Student Information", color=(0, 100, 200, 255))
            dpg.add_separator()
            
            dpg.add_text("Student Name:")
            dpg.add_input_text(tag="student_name", width=300)
            
            dpg.add_text("Candidate Number:")
            dpg.add_input_text(tag="candidate_number", width=300)
            
            dpg.add_text("School Name:")
            dpg.add_input_text(tag="school_name", width=300)
            
            dpg.add_spacer(height=20)
            
            # Subject Selection Section  
            dpg.add_text("Subject Selection", color=(0, 100, 200, 255))
            dpg.add_separator()
            
            if CAMBRIDGE_SUBJECTS:
                for subject_code, subject_info in list(CAMBRIDGE_SUBJECTS.items())[:5]:  # Limit to first 5 for simplicity
                    dpg.add_checkbox(
                        label=f"{subject_code}: {subject_info['name']}",
                        tag=f"subject_{subject_code}",
                        callback=self.on_subject_selected
                    )
            else:
                dpg.add_text("No subjects configured")
            
            dpg.add_spacer(height=20)
            
            # Grade Input Section
            dpg.add_text("Grade Input", color=(0, 100, 200, 255)) 
            dpg.add_separator()
            
            with dpg.group(tag="grade_inputs"):
                dpg.add_text("Select subjects above to enter grades")
            
            dpg.add_spacer(height=20)
            
            # Action Buttons
            dpg.add_button(
                label="Calculate Results",
                callback=self.calculate_results,
                width=200,
                height=40
            )
            
            dpg.add_same_line()
            
            dpg.add_button(
                label="Generate PDF Report", 
                callback=self.generate_pdf,
                width=200,
                height=40
            )
            
            dpg.add_spacer(height=20)
            
            # Results Section
            dpg.add_text("Results", color=(0, 100, 200, 255))
            dpg.add_separator()
            
            with dpg.group(tag="results_display"):
                dpg.add_text("No results yet. Enter grades and click Calculate Results.")
    
    def on_subject_selected(self, sender, app_data):
        """Handle subject selection"""
        subject_code = sender.replace("subject_", "")
        
        # Clear previous grade inputs
        dpg.delete_item("grade_inputs", children_only=True)
        
        # Collect all selected subjects
        self.selected_subjects = []
        for subject_code in CAMBRIDGE_SUBJECTS.keys():
            if dpg.get_value(f"subject_{subject_code}"):
                self.selected_subjects.append(subject_code)
        
        # Create grade inputs for selected subjects
        if self.selected_subjects:
            for subject_code in self.selected_subjects:
                subject_name = CAMBRIDGE_SUBJECTS[subject_code]['name']
                
                with dpg.group(parent="grade_inputs"):
                    dpg.add_text(f"{subject_code}: {subject_name}")
                    dpg.add_input_int(
                        label="Grade (0-100)",
                        tag=f"grade_{subject_code}",
                        default_value=50,
                        min_value=0,
                        max_value=100,
                        width=150
                    )
        else:
            dpg.add_text("Select subjects above to enter grades", parent="grade_inputs")
    
    def calculate_results(self):
        """Calculate and display results"""
        if not self.selected_subjects or not self.calculator:
            dpg.delete_item("results_display", children_only=True)
            dpg.add_text("Please select subjects and enter grades", parent="results_display")
            return
        
        # Collect grades
        grades = {}
        for subject_code in self.selected_subjects:
            grade_value = dpg.get_value(f"grade_{subject_code}")
            grades[subject_code] = grade_value
        
        # Calculate results
        try:
            results = self.calculator.calculate_results(grades)
            
            # Display results
            dpg.delete_item("results_display", children_only=True)
            
            dpg.add_text(f"Total Score: {results['total_score']:.1f}", parent="results_display")
            dpg.add_text(f"Average: {results['average']:.1f}%", parent="results_display")
            dpg.add_text(f"Overall Grade: {results['overall_grade']}", parent="results_display")
            
            dpg.add_spacer(height=10, parent="results_display")
            
            for subject_code, grade in grades.items():
                subject_name = CAMBRIDGE_SUBJECTS[subject_code]['name']
                dpg.add_text(f"{subject_code}: {grade}%", parent="results_display")
            
        except Exception as e:
            dpg.delete_item("results_display", children_only=True)
            dpg.add_text(f"Calculation error: {e}", parent="results_display")
    
    def generate_pdf(self):
        """Generate PDF report"""
        if not self.pdf_generator:
            dpg.delete_item("results_display", children_only=True)
            dpg.add_text("PDF generation not available", parent="results_display")
            return
        
        student_name = dpg.get_value("student_name")
        candidate_number = dpg.get_value("candidate_number")  
        school_name = dpg.get_value("school_name")
        
        if not student_name or not self.selected_subjects:
            dpg.delete_item("results_display", children_only=True)
            dpg.add_text("Please enter student name and select subjects", parent="results_display")
            return
        
        # Collect grades
        grades = {}
        for subject_code in self.selected_subjects:
            grade_value = dpg.get_value(f"grade_{subject_code}")
            grades[subject_code] = grade_value
        
        try:
            # Generate PDF
            filename = f"{student_name.replace(' ', '_')}_report.pdf"
            self.pdf_generator.generate_report({
                'student_name': student_name,
                'candidate_number': candidate_number,
                'school_name': school_name,
                'grades': grades
            }, filename)
            
            dpg.delete_item("results_display", children_only=True)
            dpg.add_text(f"PDF generated: {filename}", parent="results_display", color=(0, 150, 0, 255))
            
        except Exception as e:
            dpg.delete_item("results_display", children_only=True)
            dpg.add_text(f"PDF generation error: {e}", parent="results_display", color=(200, 0, 0, 255))

def main():
    """Main entry point"""
    try:
        app = CambridgeReportGUI()
    except Exception as e:
        print(f"Application error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()