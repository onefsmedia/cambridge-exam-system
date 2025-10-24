"""
Cambridge International Examination Report Card Generator - Dear PyGui macOS Version
Modern macOS-style interface with proper auto-resize and beautiful color theme
"""

import dearpygui.dearpygui as dpg
import json
import os
from typing import Dict, List, Any
from config import APP_SETTINGS, get_subject_names, get_subject_coefficient, CAMBRIDGE_SUBJECTS
from grade_calculator import CambridgeGradeCalculator
from pdf_generator import CambridgePDFGenerator
from settings_dialog_dpg import SettingsDialog

def get_subject_data(subject_name):
    """Get subject data by name"""
    for subject in CAMBRIDGE_SUBJECTS:
        if subject["name"] == subject_name:
            return subject
    return None

class CambridgeReportGUI:
    def __init__(self):
        """Initialize the Dear PyGui macOS application"""
        self.calculator = CambridgeGradeCalculator()
        self.pdf_generator = CambridgePDFGenerator()
        self.selected_subjects = []
        
        # Initialize variables
        self.student_name = ""
        self.candidate_number = ""
        self.examination_session = ""
        self.school_name = APP_SETTINGS['default_school']
        self.selected_subject = ""
        self.score_value = 0
        
        # Initialize Dear PyGui
        dpg.create_context()
        dpg.create_viewport(
            title=APP_SETTINGS['title'],
            width=1400,           # Increased width
            height=900,           # Increased height
            min_width=1000,       # Increased minimum width
            min_height=750,       # Increased minimum height
            resizable=True,
            vsync=True,
            maximized=False       # Start windowed, not maximized
        )
        
        # Load fonts for better typography
        self.setup_fonts()
        
        # Setup macOS-style theme
        self.setup_macos_theme()
        
        # Create the main window
        self.create_main_window()
        
    def setup_fonts(self):
        """Setup fonts with proper error handling"""
        try:
            with dpg.font_registry():
                # Use default font with different sizes (empty string uses default)
                self.regular_font = dpg.add_font("", 16)       
                self.title_font = dpg.add_font("", 32)        
                self.section_font = dpg.add_font("", 18)      
                self.subtitle_font = dpg.add_font("", 15)     
                self.button_font = dpg.add_font("", 15)       
        except Exception as e:
            print(f"Font loading error: {e}")
            # Use None as fallback - DPG will use default fonts
            self.regular_font = None
            self.title_font = None
            self.section_font = None
            self.subtitle_font = None
            self.button_font = None
    
    def setup_macos_theme(self):
        """Setup macOS-style theme with sophisticated colors"""
        with dpg.theme() as self.macos_theme:
            with dpg.theme_component(dpg.mvAll):
                # macOS Big Sur/Monterey color palette with better contrast
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (248, 249, 250, 255))     # macOS background
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (255, 255, 255, 255))     # Card background
                dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (255, 255, 255, 255))     # Popup background
                dpg.add_theme_color(dpg.mvThemeCol_Border, (200, 200, 200, 180))      # More visible border
                dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0, 255))              # Pure black text for visibility
                dpg.add_theme_color(dpg.mvThemeCol_TextDisabled, (100, 100, 100, 255)) # Darker disabled text
                
                # Modern button colors (macOS style)
                dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 122, 255, 255))        # System blue
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (10, 132, 255, 255)) # Lighter blue
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (0, 105, 217, 255))   # Darker blue
                
                # Input field colors (clean white with subtle borders)
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (255, 255, 255, 255))
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (250, 250, 250, 255))
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (255, 255, 255, 255))
                
                # Header colors
                dpg.add_theme_color(dpg.mvThemeCol_Header, (240, 240, 240, 255))
                dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (230, 230, 230, 255))
                dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (220, 220, 220, 255))
                
                # Refined styling with better spacing
                dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 12)
                dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 10)
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 6)
                dpg.add_theme_style(dpg.mvStyleVar_ScrollbarRounding, 8)
                dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 6)
                dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 24, 24)
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 14, 10)
                dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 16, 12)
                dpg.add_theme_style(dpg.mvStyleVar_ItemInnerSpacing, 10, 8)
                dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 0)
                dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 1)
        
        # Enhanced button themes with macOS colors
        with dpg.theme() as self.success_theme:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (52, 199, 89, 255))        # macOS green
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (62, 209, 99, 255))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (42, 179, 79, 255))
                dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255, 255))
        
        with dpg.theme() as self.warning_theme:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (255, 149, 0, 255))        # macOS orange
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (255, 159, 20, 255))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (235, 129, 0, 255))
                dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255, 255))
        
        with dpg.theme() as self.danger_theme:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (255, 59, 48, 255))        # macOS red
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (255, 79, 68, 255))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (235, 39, 28, 255))
                dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255, 255))
        
        with dpg.theme() as self.secondary_theme:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (246, 247, 249, 255))      # Light gray
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (236, 237, 239, 255))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (226, 227, 229, 255))
                dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 122, 255, 255))          # Blue text
    
    def create_main_window(self):
        """Create the main application window with auto-resize layout"""
        with dpg.window(label="Cambridge Report Generator", tag="main_window"):
            # Apply macOS theme
            dpg.bind_theme(self.macos_theme)
            
            # Header
            self.create_header()
            
                # Create responsive layout using groups
            with dpg.group(tag="main_content"):
                # Two-column layout that auto-resizes
                with dpg.group(horizontal=True, tag="content_columns"):
                    # Left column - Student info and subject selection
                    with dpg.child_window(tag="left_column", width=650, height=750, autosize_x=False, autosize_y=False, border=False):
                        self.create_student_info_card()
                        dpg.add_spacer(height=24)
                        self.create_subject_selection_card()
                    
                    dpg.add_spacer(width=24)
                    
                    # Right column - Grades and actions  
                    with dpg.child_window(tag="right_column", width=650, height=750, autosize_x=False, autosize_y=False, border=False):
                        self.create_grades_card()
                        dpg.add_spacer(height=24)
                        self.create_actions_card()
    
    def create_header(self):
        """Create macOS-style header with better typography"""
        if self.title_font:
            dpg.bind_font(self.title_font)
        dpg.add_text("Cambridge International Examination", color=(0, 0, 0, 255))  # Pure black for better visibility
        dpg.add_text("Report Card Generator", color=(0, 0, 0, 255))
        if self.subtitle_font:
            dpg.bind_font(self.subtitle_font)
        dpg.add_text(f"Version {APP_SETTINGS['version']} • macOS Edition", color=(142, 142, 147, 255))
        dpg.add_spacer(height=32)
        if self.regular_font:
            dpg.bind_font(self.regular_font)
    
    def bind_font_safe(self, font):
        """Safely bind font only if it exists"""
        if font:
            dpg.bind_font(font)
    
    def create_student_info_card(self):
        """Create student information card with macOS styling"""
        with dpg.child_window(label="Student Information", height=260, border=True, tag="student_info_card"):
            dpg.bind_font(self.section_font)
            dpg.add_text("Student Information", color=(28, 28, 30, 255))
            dpg.bind_font(self.regular_font)
            dpg.add_separator()
            dpg.add_spacer(height=16)
            
            # Student name
            dpg.add_text("Student Name")
            dpg.add_input_text(
                tag="student_name_input",
                width=-1,
                callback=self.on_student_name_changed,
                hint="Enter student's full name"
            )
            dpg.add_spacer(height=12)
            
            # Candidate number with generate button
            with dpg.group(horizontal=True):
                dpg.add_text("Candidate Number")
                dpg.add_spacer(width=20)
                dpg.add_button(
                    label="Generate",
                    callback=self.generate_candidate_number,
                    width=90,
                    height=28
                )
            
            dpg.add_input_text(
                tag="candidate_number_input",
                width=-1,
                callback=self.on_candidate_number_changed,
                hint="Enter or generate candidate number"
            )
            dpg.add_spacer(height=12)
            
            # Examination session
            dpg.add_text("Examination Session")
            dpg.add_combo(
                items=APP_SETTINGS['examination_sessions'],
                tag="session_combo",
                width=-1,
                callback=self.on_session_changed,
                default_value=APP_SETTINGS['examination_sessions'][0]
            )
            dpg.add_spacer(height=12)
            
            # School name
            dpg.add_text("School Name")
            dpg.add_input_text(
                tag="school_name_input",
                width=-1,
                callback=self.on_school_name_changed,
                default_value=APP_SETTINGS['default_school']
            )
    
    def create_subject_selection_card(self):
        """Create subject selection card"""
        with dpg.child_window(label="Subject Selection", height=320, border=True, tag="subject_selection_card"):
            dpg.bind_font(self.section_font)
            dpg.add_text("Subject Selection", color=(28, 28, 30, 255))
            dpg.bind_font(self.regular_font)
            dpg.add_separator()
            dpg.add_spacer(height=16)
            
            # Subject combo
            dpg.add_text("Select Subject")
            dpg.add_combo(
                items=get_subject_names(),
                tag="subject_combo",
                width=-1,
                callback=self.on_subject_selected
            )
            dpg.add_spacer(height=12)
            
            # Score input
            dpg.add_text("Score (0-100)")
            dpg.add_input_int(
                tag="score_input",
                width=-1,
                min_value=0,
                max_value=100,
                callback=self.on_score_changed
            )
            dpg.add_spacer(height=16)
            
            # Add and Settings buttons
            with dpg.group(horizontal=True):
                dpg.add_button(
                    label="Add Subject",
                    tag="add_subject_btn",
                    callback=self.add_subject,
                    enabled=False,
                    width=140,
                    height=36
                )
                
                dpg.add_spacer(width=16)
                
                dpg.add_button(
                    label="Settings",
                    callback=self.show_settings,
                    width=120,
                    height=36
                )
                dpg.bind_item_theme(dpg.last_item(), self.secondary_theme)
    
    def create_grades_card(self):
        """Create grades display card with auto-resize table"""
        with dpg.child_window(label="Current Grades", height=420, border=True, tag="grades_card"):
            dpg.bind_font(self.section_font)
            dpg.add_text("Current Grades", color=(28, 28, 30, 255))
            dpg.bind_font(self.regular_font)
            dpg.add_separator()
            dpg.add_spacer(height=16)
            
            # Auto-resizing table for grades
            with dpg.table(
                tag="grades_table",
                header_row=True,
                borders_innerH=True,
                borders_outerH=True,
                borders_innerV=True,
                borders_outerV=True,
                scrollY=True,
                height=280,
                resizable=True
            ):
                dpg.add_table_column(label="Subject", width_fixed=False, init_width_or_weight=0.5)
                dpg.add_table_column(label="Score", width_fixed=False, init_width_or_weight=0.2)
                dpg.add_table_column(label="Grade", width_fixed=False, init_width_or_weight=0.15)
                dpg.add_table_column(label="Actions", width_fixed=False, init_width_or_weight=0.25)
            
            dpg.add_spacer(height=16)
            
            # Action buttons for selected subject
            with dpg.group(horizontal=True):
                dpg.add_button(
                    label="Remove Selected",
                    tag="remove_subject_btn",
                    callback=self.remove_subject,
                    enabled=False,
                    width=140,
                    height=32
                )
                dpg.bind_item_theme(dpg.last_item(), self.danger_theme)
                
                dpg.add_spacer(width=16)
                
                dpg.add_button(
                    label="Edit Selected",
                    tag="edit_subject_btn", 
                    callback=self.edit_subject,
                    enabled=False,
                    width=120,
                    height=32
                )
                dpg.bind_item_theme(dpg.last_item(), self.secondary_theme)
    
    def create_actions_card(self):
        """Create actions card with generate, sample, etc."""
        with dpg.child_window(label="Actions", height=200, border=True, tag="actions_card"):
            dpg.bind_font(self.section_font)
            dpg.add_text("Actions", color=(28, 28, 30, 255))
            dpg.bind_font(self.regular_font)
            dpg.add_separator()
            dpg.add_spacer(height=16)
            
            # Action buttons with better spacing
            dpg.add_button(
                label="Clear All Data",
                callback=self.clear_all_data,
                width=-1,
                height=40
            )
            dpg.bind_item_theme(dpg.last_item(), self.warning_theme)
            
            dpg.add_spacer(height=12)
            
            dpg.add_button(
                label="Load Sample Data",
                callback=self.load_sample_data,
                width=-1,
                height=40
            )
            dpg.bind_item_theme(dpg.last_item(), self.secondary_theme)
            
            dpg.add_spacer(height=12)
            
            dpg.add_button(
                label="Generate PDF Report",
                tag="generate_report_btn",
                callback=self.generate_report,
                width=-1,
                height=44,
                enabled=False
            )
            dpg.bind_item_theme(dpg.last_item(), self.success_theme)
    
    def setup_auto_resize(self):
        """Setup auto-resize callbacks for responsive design"""
        def resize_callback():
            viewport_width = dpg.get_viewport_width()
            viewport_height = dpg.get_viewport_height()
            
            # Calculate responsive column widths
            available_width = viewport_width - 100  # Account for padding
            column_width = (available_width - 24) // 2  # 24px for spacing between columns
            
            # Update column widths
            dpg.set_item_width("left_column", column_width)
            dpg.set_item_width("right_column", column_width)
            
            # Update card heights based on viewport
            card_height = max(200, (viewport_height - 200) // 3)
            dpg.set_item_height("student_info_card", min(260, card_height))
            dpg.set_item_height("subject_selection_card", min(320, card_height))
            dpg.set_item_height("grades_card", min(420, card_height * 1.5))
            dpg.set_item_height("actions_card", min(200, card_height * 0.8))
        
        # Set resize callback
        dpg.set_viewport_resize_callback(resize_callback)
    
    def run(self):
        """Run the application"""
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("main_window", True)
        
        # Setup auto-resize after showing viewport
        self.setup_auto_resize()
        
        dpg.start_dearpygui()
        dpg.destroy_context()
    
    # Callback methods (keeping all existing callback functionality)
    def on_student_name_changed(self, sender, app_data):
        """Handle student name change"""
        self.student_name = app_data
        self.update_generate_button_state()
    
    def on_candidate_number_changed(self, sender, app_data):
        """Handle candidate number change"""
        self.candidate_number = app_data
        self.update_generate_button_state()
    
    def on_session_changed(self, sender, app_data):
        """Handle examination session change"""
        self.examination_session = app_data
        self.update_generate_button_state()
    
    def on_school_name_changed(self, sender, app_data):
        """Handle school name change"""
        self.school_name = app_data
    
    def on_subject_selected(self, sender, app_data):
        """Handle subject selection"""
        self.selected_subject = app_data
        self.update_add_subject_button_state()
    
    def on_score_changed(self, sender, app_data):
        """Handle score change"""
        self.score_value = app_data
        self.update_add_subject_button_state()
    
    def generate_candidate_number(self):
        """Generate a new candidate number"""
        import random
        candidate_number = f"{random.randint(1000, 9999)}{random.randint(100, 999)}"
        dpg.set_value("candidate_number_input", candidate_number)
        self.candidate_number = candidate_number
        self.update_generate_button_state()
    
    def update_add_subject_button_state(self):
        """Update add subject button state"""
        can_add = (self.selected_subject and 
                  0 <= self.score_value <= 100 and
                  not any(s['name'] == self.selected_subject for s in self.selected_subjects))
        dpg.configure_item("add_subject_btn", enabled=can_add)
    
    def update_generate_button_state(self):
        """Update generate report button state"""
        can_generate = (self.student_name.strip() and 
                       self.candidate_number.strip() and
                       self.examination_session and
                       len(self.selected_subjects) > 0)
        dpg.configure_item("generate_report_btn", enabled=can_generate)
    
    def add_subject(self):
        """Add subject to the grades table"""
        if not self.selected_subject or self.score_value < 0 or self.score_value > 100:
            return
        
        # Check for duplicates
        if any(s['name'] == self.selected_subject for s in self.selected_subjects):
            return
        
        subject_data = get_subject_data(self.selected_subject)
        if not subject_data:
            return
        
        grade = self.calculator.score_to_grade(self.score_value)
        
        subject_entry = {
            'name': self.selected_subject,
            'score': self.score_value,
            'grade': grade,
            'data': subject_data
        }
        
        self.selected_subjects.append(subject_entry)
        self.refresh_grades_table()
        
        # Clear selections
        dpg.set_value("subject_combo", "")
        dpg.set_value("score_input", 0)
        self.selected_subject = ""
        self.score_value = 0
        self.update_add_subject_button_state()
        self.update_generate_button_state()
    
    def refresh_grades_table(self):
        """Refresh the grades table"""
        # Clear existing rows
        for i in range(len(self.selected_subjects)):
            if dpg.does_item_exist(f"table_row_{i}"):
                dpg.delete_item(f"table_row_{i}")
        
        # Add current subjects
        for i, subject in enumerate(self.selected_subjects):
            with dpg.table_row(tag=f"table_row_{i}", parent="grades_table"):
                dpg.add_text(subject['name'])
                dpg.add_text(str(subject['score']))
                dpg.add_text(subject['grade'])
                with dpg.group(horizontal=True):
                    dpg.add_button(
                        label="Edit",
                        callback=lambda s, a, u=i: self.edit_subject_by_index(u),
                        width=50,
                        height=24
                    )
                    dpg.add_button(
                        label="Remove",
                        callback=lambda s, a, u=i: self.remove_subject_by_index(u),
                        width=60,
                        height=24
                    )
                    dpg.bind_item_theme(dpg.last_item(), self.danger_theme)
    
    def edit_subject_by_index(self, index):
        """Edit subject by table index"""
        if 0 <= index < len(self.selected_subjects):
            # For now, just remove and let user re-add
            self.remove_subject_by_index(index)
    
    def remove_subject_by_index(self, index):
        """Remove subject by table index"""
        if 0 <= index < len(self.selected_subjects):
            self.selected_subjects.pop(index)
            self.refresh_grades_table()
            self.update_generate_button_state()
    
    def remove_subject(self):
        """Remove selected subject (placeholder)"""
        pass
    
    def edit_subject(self):
        """Edit selected subject (placeholder)"""
        pass
    
    def clear_all_data(self):
        """Clear all data"""
        self.selected_subjects.clear()
        self.refresh_grades_table()
        
        # Clear inputs
        dpg.set_value("student_name_input", "")
        dpg.set_value("candidate_number_input", "")
        dpg.set_value("school_name_input", APP_SETTINGS['default_school'])
        dpg.set_value("subject_combo", "")
        dpg.set_value("score_input", 0)
        
        # Reset variables
        self.student_name = ""
        self.candidate_number = ""
        self.school_name = APP_SETTINGS['default_school']
        self.selected_subject = ""
        self.score_value = 0
        
        self.update_add_subject_button_state()
        self.update_generate_button_state()
    
    def load_sample_data(self):
        """Load sample data for testing"""
        # Clear existing data first
        self.clear_all_data()
        
        # Set sample student info
        sample_name = "John Smith"
        sample_number = "123456789"
        sample_session = "May/June 2024"
        
        dpg.set_value("student_name_input", sample_name)
        dpg.set_value("candidate_number_input", sample_number)
        dpg.set_value("session_combo", sample_session)
        
        self.student_name = sample_name
        self.candidate_number = sample_number
        self.examination_session = sample_session
        
        # Add sample subjects
        sample_subjects = [
            ("Mathematics", 85),
            ("Physics", 78),
            ("Chemistry", 82),
            ("English Literature", 88)
        ]
        
        for subject_name, score in sample_subjects:
            subject_data = get_subject_data(subject_name)
            if subject_data:
                grade = self.calculator.score_to_grade(score)
                subject_entry = {
                    'name': subject_name,
                    'score': score,
                    'grade': grade,
                    'data': subject_data
                }
                self.selected_subjects.append(subject_entry)
        
        self.refresh_grades_table()
        self.update_generate_button_state()
    
    def show_settings(self):
        """Show settings dialog (placeholder)"""
        print("Settings dialog would open here")
    
    def generate_report(self):
        """Generate PDF report"""
        if not self.student_name.strip() or not self.candidate_number.strip():
            return
        
        try:
            # Calculate final grade
            final_result = self.calculator.calculate_final_grade(self.selected_subjects)
            
            # Prepare student data
            student_data = {
                'name': self.student_name,
                'candidate_number': self.candidate_number,
                'examination_session': self.examination_session,
                'school': self.school_name,
                'subjects': self.selected_subjects,
                'final_grade': final_result['grade'],
                'total_points': final_result['total_points'],
                'points_breakdown': final_result['points_breakdown']
            }
            
            # Generate PDF
            filepath = self.pdf_generator.generate_report(student_data)
            
            # Show success message
            print(f"Report generated successfully: {filepath}")
            
        except Exception as e:
            print(f"Error generating report: {str(e)}")


if __name__ == "__main__":
    app = CambridgeReportGUI()
    app.run()
    
    def create_student_info_card(self):
        """Create student information card with iOS styling"""
        with dpg.child_window(label="Student Information", height=200, border=True):
            dpg.add_text("Student Information", color=(29, 29, 31, 255))
            dpg.add_separator()
            dpg.add_spacing(count=2)
            
            # Student name
            dpg.add_text("Student Name:")
            dpg.add_input_text(
                tag="student_name_input",
                width=-1,
                callback=self.on_student_name_changed,
                hint="Enter student's full name"
            )
            dpg.add_spacing()
            
            # Candidate number
            with dpg.group(horizontal=True):
                dpg.add_text("Candidate Number:")
                dpg.add_button(
                    label="Generate",
                    callback=self.generate_candidate_number,
                    width=80,
                    height=25
                )
            
            dpg.add_input_text(
                tag="candidate_number_input",
                width=-1,
                callback=self.on_candidate_number_changed,
                hint="Enter or generate candidate number"
            )
            dpg.add_spacing()
            
            # Examination session
            dpg.add_text("Examination Session:")
            examination_sessions = ["May/June 2024", "October/November 2024", "February/March 2025", "May/June 2025"]
            dpg.add_combo(
                items=examination_sessions,
                tag="session_combo",
                width=-1,
                callback=self.on_session_changed,
                default_value=examination_sessions[0]
            )
            dpg.add_spacer(height=10)
            
            # School name
            dpg.add_text("School Name:")
            dpg.add_input_text(
                tag="school_name_input",
                width=-1,
                callback=self.on_school_name_changed,
                default_value=APP_SETTINGS['default_school']
            )
    
    def create_subject_selection_card(self):
        """Create subject selection card"""
        with dpg.child_window(label="Subject Selection", height=300, border=True):
            dpg.add_text("Subject Selection", color=(29, 29, 31, 255))
            dpg.add_separator()
            dpg.add_spacer(height=10)
            
            # Subject combo
            dpg.add_text("Select Subject:")
            dpg.add_combo(
                items=get_subject_names(),
                tag="subject_combo",
                width=-1,
                callback=self.on_subject_selected
            )
            dpg.add_spacer(height=10)
            
            # Score input
            dpg.add_text("Score (0-100):")
            dpg.add_input_int(
                tag="score_input",
                width=-1,
                min_value=0,
                max_value=100,
                callback=self.on_score_changed
            )
            dpg.add_spacer(height=10)
            
            # Add and Settings buttons
            with dpg.group(horizontal=True):
                dpg.add_button(
                    label="Add Subject",
                    tag="add_subject_btn",
                    callback=self.add_subject,
                    enabled=False,
                    width=120
                )
                
                dpg.add_button(
                    label="Settings",
                    callback=self.show_settings,
                    width=100
                )
                dpg.bind_item_theme(dpg.last_item(), self.secondary_theme)
    
    def create_grades_card(self):
        """Create grades display card"""
        with dpg.child_window(label="Current Grades", height=400, border=True):
            dpg.add_text("Current Grades", color=(29, 29, 31, 255))
            dpg.add_separator()
            dpg.add_spacing(count=2)
            
            # Table for grades
            with dpg.table(
                tag="grades_table",
                header_row=True,
                borders_innerH=True,
                borders_outerH=True,
                borders_innerV=True,
                borders_outerV=True,
                scrollY=True,
                height=300
            ):
                dpg.add_table_column(label="Subject", width_fixed=True, init_width_or_weight=200)
                dpg.add_table_column(label="Score", width_fixed=True, init_width_or_weight=60)
                dpg.add_table_column(label="Grade", width_fixed=True, init_width_or_weight=60)
                dpg.add_table_column(label="Actions", width_fixed=True, init_width_or_weight=100)
            
            dpg.add_spacing(count=2)
            
            # Action buttons for selected subject
            with dpg.group(horizontal=True):
                dpg.add_button(
                    label="Remove",
                    tag="remove_subject_btn",
                    callback=self.remove_subject,
                    enabled=False,
                    width=80
                )
                dpg.bind_item_theme(dpg.last_item(), self.danger_theme)
                
                dpg.add_button(
                    label="Edit",
                    tag="edit_subject_btn", 
                    callback=self.edit_subject,
                    enabled=False,
                    width=80
                )
                dpg.bind_item_theme(dpg.last_item(), self.secondary_theme)
    
    def create_actions_card(self):
        """Create actions card with generate, sample, etc."""
        with dpg.child_window(label="Actions", height=180, border=True):
            dpg.add_text("Actions", color=(29, 29, 31, 255))
            dpg.add_separator()
            dpg.add_spacing(count=2)
            
            # Action buttons
            with dpg.group():
                dpg.add_button(
                    label="Clear All Data",
                    callback=self.clear_all_data,
                    width=-1,
                    height=35
                )
                dpg.bind_item_theme(dpg.last_item(), self.warning_theme)
                
                dpg.add_spacing()
                
                dpg.add_button(
                    label="Load Sample Data",
                    callback=self.load_sample_data,
                    width=-1,
                    height=35
                )
                dpg.bind_item_theme(dpg.last_item(), self.secondary_theme)
                
                dpg.add_spacing()
                
                dpg.add_button(
                    label="Generate Report",
                    tag="generate_report_btn",
                    callback=self.generate_report,
                    width=-1,
                    height=40,
                    enabled=False
                )
                dpg.bind_item_theme(dpg.last_item(), self.success_theme)
    
    def run(self):
        """Run the application"""
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("main_window", True)
        dpg.start_dearpygui()
        dpg.destroy_context()
    
    # Callback methods
    def on_student_name_changed(self, sender, app_data):
        """Handle student name change"""
        self.student_name = app_data
        self.update_generate_button_state()
    
    def on_candidate_number_changed(self, sender, app_data):
        """Handle candidate number change"""
        self.candidate_number = app_data
        self.update_generate_button_state()
    
    def on_session_changed(self, sender, app_data):
        """Handle examination session change"""
        self.examination_session = app_data
        self.update_generate_button_state()
    
    def on_school_name_changed(self, sender, app_data):
        """Handle school name change"""
        self.school_name = app_data
    
    def on_subject_selected(self, sender, app_data):
        """Handle subject selection"""
        self.selected_subject = app_data
        self.update_add_subject_button_state()
    
    def on_score_changed(self, sender, app_data):
        """Handle score change"""
        self.score_value = app_data
        self.update_add_subject_button_state()
    
    def generate_candidate_number(self):
        """Generate a new candidate number"""
        import random
        candidate_number = f"{random.randint(1000, 9999)}{random.randint(100, 999)}"
        dpg.set_value("candidate_number_input", candidate_number)
        self.candidate_number = candidate_number
        self.update_generate_button_state()
    
    def update_add_subject_button_state(self):
        """Update add subject button state"""
        can_add = (self.selected_subject and 
                  0 <= self.score_value <= 100 and
                  not any(s['name'] == self.selected_subject for s in self.selected_subjects))
        dpg.configure_item("add_subject_btn", enabled=can_add)
    
    def update_generate_button_state(self):
        """Update generate report button state"""
        can_generate = (self.student_name.strip() and 
                       self.candidate_number.strip() and
                       self.examination_session and
                       len(self.selected_subjects) > 0)
        dpg.configure_item("generate_report_btn", enabled=can_generate)
    
    def add_subject(self):
        """Add subject to the grades table"""
        if not self.selected_subject or self.score_value < 0 or self.score_value > 100:
            return
        
        # Check for duplicates
        if any(s['name'] == self.selected_subject for s in self.selected_subjects):
            return
        
        subject_data = get_subject_data(self.selected_subject)
        if not subject_data:
            return
        
        grade = self.calculator.score_to_grade(self.score_value)
        
        subject_entry = {
            'name': self.selected_subject,
            'score': self.score_value,
            'grade': grade,
            'data': subject_data
        }
        
        self.selected_subjects.append(subject_entry)
        self.refresh_grades_table()
        
        # Clear selections
        dpg.set_value("subject_combo", "")
        dpg.set_value("score_input", 0)
        self.selected_subject = ""
        self.score_value = 0
        self.update_add_subject_button_state()
        self.update_generate_button_state()
    
    def refresh_grades_table(self):
        """Refresh the grades table"""
        # Clear existing rows
        for i in range(len(self.selected_subjects)):
            if dpg.does_item_exist(f"table_row_{i}"):
                dpg.delete_item(f"table_row_{i}")
        
        # Add current subjects
        for i, subject in enumerate(self.selected_subjects):
            with dpg.table_row(tag=f"table_row_{i}", parent="grades_table"):
                dpg.add_text(subject['name'])
                dpg.add_text(str(subject['score']))
                dpg.add_text(subject['grade'])
                with dpg.group(horizontal=True):
                    dpg.add_button(
                        label="Edit",
                        callback=lambda s, a, u=i: self.edit_subject_by_index(u),
                        width=40,
                        height=20
                    )
                    dpg.add_button(
                        label="Del",
                        callback=lambda s, a, u=i: self.remove_subject_by_index(u),
                        width=40,
                        height=20
                    )
                    dpg.bind_item_theme(dpg.last_item(), self.danger_theme)
    
    def edit_subject_by_index(self, index):
        """Edit subject by table index"""
        if 0 <= index < len(self.selected_subjects):
            # For now, just remove and let user re-add
            # In a full implementation, you'd open an edit dialog
            self.remove_subject_by_index(index)
    
    def remove_subject_by_index(self, index):
        """Remove subject by table index"""
        if 0 <= index < len(self.selected_subjects):
            self.selected_subjects.pop(index)
            self.refresh_grades_table()
            self.update_generate_button_state()
    
    def remove_subject(self):
        """Remove selected subject (placeholder)"""
        pass
    
    def edit_subject(self):
        """Edit selected subject (placeholder)"""
        pass
    
    def clear_all_data(self):
        """Clear all data"""
        self.selected_subjects.clear()
        self.refresh_grades_table()
        
        # Clear inputs
        dpg.set_value("student_name_input", "")
        dpg.set_value("candidate_number_input", "")
        dpg.set_value("school_name_input", APP_SETTINGS['default_school'])
        dpg.set_value("subject_combo", "")
        dpg.set_value("score_input", 0)
        
        # Reset variables
        self.student_name = ""
        self.candidate_number = ""
        self.school_name = APP_SETTINGS['default_school']
        self.selected_subject = ""
        self.score_value = 0
        
        self.update_add_subject_button_state()
        self.update_generate_button_state()
    
    def load_sample_data(self):
        """Load sample data for testing"""
        # Clear existing data first
        self.clear_all_data()
        
        # Set sample student info
        sample_name = "John Smith"
        sample_number = "123456789"
        sample_session = "May/June 2024"
        
        dpg.set_value("student_name_input", sample_name)
        dpg.set_value("candidate_number_input", sample_number)
        dpg.set_value("session_combo", sample_session)
        
        self.student_name = sample_name
        self.candidate_number = sample_number
        self.examination_session = sample_session
        
        # Add sample subjects
        sample_subjects = [
            ("Mathematics", 85),
            ("Physics", 78),
            ("Chemistry", 82),
            ("English Language", 88)
        ]
        
        for subject_name, score in sample_subjects:
            subject_data = get_subject_data(subject_name)
            if subject_data:
                grade = self.calculator.score_to_grade(score)
                subject_entry = {
                    'name': subject_name,
                    'score': score,
                    'grade': grade,
                    'data': subject_data
                }
                self.selected_subjects.append(subject_entry)
        
        self.refresh_grades_table()
        self.update_generate_button_state()
    
    def show_settings(self):
        """Show settings dialog (placeholder)"""
        pass
    
    def generate_report(self):
        """Generate PDF report"""
        if not self.student_name.strip() or not self.candidate_number.strip():
            return
        
        try:
            # Calculate final grade
            final_result = self.calculator.calculate_final_grade(self.selected_subjects)
            
            # Prepare student data
            student_data = {
                'name': self.student_name,
                'candidate_number': self.candidate_number,
                'examination_session': self.examination_session,
                'school': self.school_name,
                'subjects': self.selected_subjects,
                'final_grade': final_result['grade'],
                'total_points': final_result['total_points'],
                'points_breakdown': final_result['points_breakdown']
            }
            
            # Generate PDF
            filepath = self.pdf_generator.generate_report(student_data)
            
            # Show success message (simplified for now)
            print(f"Report generated successfully: {filepath}")
            
        except Exception as e:
            print(f"Error generating report: {str(e)}")


if __name__ == "__main__":
    app = CambridgeReportGUI()
    app.run()