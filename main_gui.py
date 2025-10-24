"""
Main GUI Interface for Cambridge Exam Report Card Generator
Uses tkinter for cross-platform compatibility
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from datetime import datetime
import os

from config import CAMBRIDGE_SUBJECTS, APP_SETTINGS, get_subject_coefficient, get_subject_names, generate_candidate_number
from grade_calculator import CambridgeGradeCalculator
from pdf_generator import CambridgePDFGenerator
from settings_dialog import show_settings_dialog
from subject_edit_dialog import SubjectEditDialog
from theme_manager import theme_manager
from theme_dialog import show_theme_dialog

class CambridgeReportGUI:
    """Main GUI application for Cambridge report card generation"""
    
    def __init__(self, root):
        self.root = root
        self.calculator = CambridgeGradeCalculator()
        self.pdf_generator = CambridgePDFGenerator()
        
        # Initialize theme manager
        self.theme_manager = theme_manager
        
        # Data storage
        self.selected_subjects = []
        self.subject_data = {}
        
        self.setup_window()
        self.create_widgets()
        
    def setup_window(self):
        """Configure the main window"""
        self.root.title(APP_SETTINGS['title'])
        self.root.resizable(True, True)
        
        # Load user's preferred theme
        theme_manager.load_theme_preference()
        
        # Configure style with theme
        self.setup_themed_styles()
        
        # Set background color to iOS system background
        ios_background = '#f2f2f7'  # iOS system background
        self.root.configure(bg=ios_background)
        
        # Main frame with Apple background
        self.main_frame = ttk.Frame(self.root, padding="20")  # Apple-style generous padding
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # No special styling needed - use Apple defaults
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Configure main frame grid weights for better content distribution
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.columnconfigure(2, weight=1)
        
        # Allow rows to expand as needed
        for i in range(6):  # Accommodate all sections
            self.main_frame.rowconfigure(i, weight=0)
        self.main_frame.rowconfigure(3, weight=1)  # Grades section should expand
    
    def setup_themed_styles(self):
        """Configure styles using theme manager"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Apply current theme to style
        theme_manager.apply_theme_to_style(style)
    
    def apply_current_theme(self):
        """Apply the current theme to the application"""
        # Reapply themed styles
        self.setup_themed_styles()
        
        # Keep iOS system background for main window
        ios_background = '#f2f2f7'  # iOS system background
        self.root.configure(bg=ios_background)
    
    def create_widgets(self):
        """Create all GUI widgets"""
        self.create_header()
        self.create_student_info_section()
        self.create_subject_selection_section()
        self.create_grades_section()
        self.create_final_grade_section()
        self.create_action_buttons()
        
        # Auto-size the window after all widgets are created
        self.auto_size_window()
    
    def create_header(self):
        """Create the application header"""
        header_frame = ttk.LabelFrame(self.main_frame, text="Cambridge Report Card Generator", 
                                     padding="20")
        header_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        
        title_label = ttk.Label(
            header_frame, 
            text="Cambridge International Examination Report Card Generator",
            style="Title.TLabel"
        )
        title_label.grid(row=0, column=0, columnspan=2)
        
        version_label = ttk.Label(
            header_frame,
            text=f"Version {APP_SETTINGS['version']} • iOS Edition",
            style="Subtitle.TLabel"
        )
        version_label.grid(row=1, column=0, columnspan=2, pady=(8, 0))
    
    def create_student_info_section(self):
        """Create student information input section"""
        info_frame = ttk.LabelFrame(self.main_frame, text="Student Information", 
                                   padding="15")
        info_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Student name
        ttk.Label(info_frame, text="Student Name:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.student_name_var = tk.StringVar()
        self.student_name_entry = ttk.Entry(info_frame, textvariable=self.student_name_var, 
                                           width=30)
        self.student_name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 20))
        
        # Candidate number with auto-generation
        ttk.Label(info_frame, text="Candidate Number:", style="Header.TLabel").grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        self.candidate_number_var = tk.StringVar(value=generate_candidate_number())
        candidate_frame = ttk.Frame(info_frame)
        candidate_frame.grid(row=0, column=3, sticky=(tk.W, tk.E))
        
        self.candidate_number_entry = ttk.Entry(candidate_frame, textvariable=self.candidate_number_var, 
                                               width=15, style="Modern.TEntry")
        self.candidate_number_entry.grid(row=0, column=0, padx=(0, 8))
        
        generate_btn = ttk.Button(candidate_frame, text="Generate", command=self.generate_new_candidate_number, 
                                 width=8, style="Secondary.TButton")
        generate_btn.grid(row=0, column=1)
        
        # Exam session
        ttk.Label(info_frame, text="Exam Session:", style="Header.TLabel").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(15, 0))
        self.exam_session_var = tk.StringVar(value=f"June {datetime.now().year}")
        self.exam_session_entry = ttk.Entry(info_frame, textvariable=self.exam_session_var, 
                                           width=30, style="Modern.TEntry")
        self.exam_session_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 20), pady=(15, 0))
        
        # School name
        ttk.Label(info_frame, text="School:", style="Header.TLabel").grid(row=1, column=2, sticky=tk.W, padx=(0, 10), pady=(15, 0))
        self.school_var = tk.StringVar(value=APP_SETTINGS['default_school'])
        self.school_entry = ttk.Entry(info_frame, textvariable=self.school_var, 
                                     width=30, style="Modern.TEntry")
        self.school_entry.grid(row=1, column=3, sticky=(tk.W, tk.E), pady=(15, 0))
        
        # Configure column weights
        info_frame.columnconfigure(1, weight=1)
        info_frame.columnconfigure(3, weight=1)
    
    def create_subject_selection_section(self):
        """Create subject selection section"""
        selection_frame = ttk.LabelFrame(self.main_frame, text="Subject Selection", 
                                        padding="15")
        selection_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Subject selection
        ttk.Label(selection_frame, text="Select Subject:", style="Header.TLabel").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.subject_var = tk.StringVar()
        self.subject_combo = ttk.Combobox(
            selection_frame,
            textvariable=self.subject_var,
            values=get_subject_names(),
            state="readonly",
            width=25,
            style="Modern.TCombobox"
        )
        self.subject_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 20))
        self.subject_combo.bind('<<ComboboxSelected>>', self.on_subject_selected)
        
        # Coefficient display
        ttk.Label(selection_frame, text="Coefficient:", style="Header.TLabel").grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        self.coefficient_var = tk.StringVar(value="Select a subject")
        self.coefficient_label = ttk.Label(selection_frame, textvariable=self.coefficient_var, font=('Arial', 10, 'bold'))
        self.coefficient_label.grid(row=0, column=3, sticky=tk.W, padx=(0, 20))
        
        # Score input
        ttk.Label(selection_frame, text="Raw Score (0-100):").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.score_var = tk.StringVar()
        self.score_entry = ttk.Entry(selection_frame, textvariable=self.score_var, width=15)
        self.score_entry.grid(row=1, column=1, sticky=tk.W, pady=(10, 0))
        
        # Grade display
        ttk.Label(selection_frame, text="Calculated Grade:").grid(row=1, column=2, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.grade_var = tk.StringVar(value="Enter score")
        self.grade_label = ttk.Label(selection_frame, textvariable=self.grade_var, font=('Arial', 10, 'bold'))
        self.grade_label.grid(row=1, column=3, sticky=tk.W, pady=(10, 0))
        
        # Bind score entry to calculate grade
        self.score_var.trace('w', self.on_score_changed)
        
        # Teacher comment
        ttk.Label(selection_frame, text="Teacher Comment:").grid(row=2, column=0, sticky=(tk.W, tk.N), padx=(0, 10), pady=(10, 0))
        self.comment_text = scrolledtext.ScrolledText(selection_frame, height=4, width=60)
        self.comment_text.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0), padx=(0, 20))
        
        # Add subject button
        self.add_subject_btn = ttk.Button(
            selection_frame,
            text="Add Subject",
            command=self.add_subject,
            state="disabled"
        )
        self.add_subject_btn.grid(row=2, column=3, sticky=(tk.W, tk.N), pady=(10, 0))
        
        # Settings button
        self.settings_btn = ttk.Button(
            selection_frame,
            text="Settings",
            command=self.show_settings,
            width=10
        )
        self.settings_btn.grid(row=3, column=3, sticky=(tk.W, tk.N), pady=(5, 0))
        
        # Configure column weights
        selection_frame.columnconfigure(1, weight=1)
        selection_frame.columnconfigure(2, weight=1)
    
    def create_grades_section(self):
        """Create section to display added subjects and grades"""
        grades_frame = ttk.LabelFrame(self.main_frame, text="Subject Grades", padding="10")
        grades_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Create treeview for displaying subjects
        columns = ('Subject', 'Coefficient', 'Score', 'Grade', 'Weighted Score', 'Comment Preview')
        self.grades_tree = ttk.Treeview(grades_frame, columns=columns, show='headings', height=8)
        
        # Configure columns
        self.grades_tree.heading('Subject', text='Subject')
        self.grades_tree.heading('Coefficient', text='Coefficient')
        self.grades_tree.heading('Score', text='Score')
        self.grades_tree.heading('Grade', text='Grade')
        self.grades_tree.heading('Weighted Score', text='Weighted Score')
        self.grades_tree.heading('Comment Preview', text='Comment Preview')
        
        # Set column widths
        self.grades_tree.column('Subject', width=120)
        self.grades_tree.column('Coefficient', width=80)
        self.grades_tree.column('Score', width=60)
        self.grades_tree.column('Grade', width=60)
        self.grades_tree.column('Weighted Score', width=100)
        self.grades_tree.column('Comment Preview', width=200)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(grades_frame, orient=tk.VERTICAL, command=self.grades_tree.yview)
        self.grades_tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid the widgets
        self.grades_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Subject management buttons
        button_frame = ttk.Frame(grades_frame)
        button_frame.grid(row=1, column=0, pady=(10, 0), sticky=tk.W)
        
        self.remove_subject_btn = ttk.Button(
            button_frame,
            text="Remove Selected Subject",
            command=self.remove_subject,
            state="disabled"
        )
        self.remove_subject_btn.grid(row=0, column=0, padx=(0, 10))
        
        self.edit_subject_btn = ttk.Button(
            button_frame,
            text="Edit Selected Subject",
            command=self.edit_subject,
            state="disabled"
        )
        self.edit_subject_btn.grid(row=0, column=1)
        
        # Bind selection event
        self.grades_tree.bind('<<TreeviewSelect>>', self.on_subject_tree_select)
        
        # Configure weights
        grades_frame.columnconfigure(0, weight=1)
        grades_frame.rowconfigure(0, weight=1)
    
    def create_final_grade_section(self):
        """Create final grade display section"""
        final_frame = ttk.LabelFrame(self.main_frame, text="Final Grade Summary", padding="10")
        final_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Total weighted score
        ttk.Label(final_frame, text="Total Weighted Score:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.total_weighted_var = tk.StringVar(value="0.00")
        ttk.Label(final_frame, textvariable=self.total_weighted_var, font=('Arial', 10, 'bold')).grid(row=0, column=1, sticky=tk.W)
        
        # Total coefficient
        ttk.Label(final_frame, text="Total Coefficient:").grid(row=0, column=2, sticky=tk.W, padx=(20, 10))
        self.total_coefficient_var = tk.StringVar(value="0.00")
        ttk.Label(final_frame, textvariable=self.total_coefficient_var, font=('Arial', 10, 'bold')).grid(row=0, column=3, sticky=tk.W)
        
        # Weighted average
        ttk.Label(final_frame, text="Weighted Average:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.weighted_average_var = tk.StringVar(value="0.00%")
        ttk.Label(final_frame, textvariable=self.weighted_average_var, font=('Arial', 12, 'bold')).grid(row=1, column=1, sticky=tk.W, pady=(10, 0))
        
        # Final grade
        ttk.Label(final_frame, text="Final Cambridge Grade:").grid(row=1, column=2, sticky=tk.W, padx=(20, 10), pady=(10, 0))
        self.final_grade_var = tk.StringVar(value="N/A")
        final_grade_label = ttk.Label(
            final_frame,
            textvariable=self.final_grade_var,
            font=('Arial', 14, 'bold'),
            foreground='darkblue'
        )
        final_grade_label.grid(row=1, column=3, sticky=tk.W, pady=(10, 0))
    
    def create_action_buttons(self):
        """Create action buttons"""
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=(20, 0), sticky=(tk.W, tk.E))
        
        # Configure column weights to push generate button to the right
        button_frame.columnconfigure(0, weight=1)
        
        # Left side buttons
        left_frame = ttk.Frame(button_frame)
        left_frame.grid(row=0, column=0, sticky=tk.W)
        
        # Clear all button
        self.clear_all_btn = ttk.Button(
            left_frame,
            text="Clear All",
            command=self.clear_all_data,
            style="Warning.TButton"
        )
        self.clear_all_btn.grid(row=0, column=0, padx=(0, 15))
        
        # Generate sample button
        self.sample_btn = ttk.Button(
            left_frame,
            text="Load Sample Data",
            command=self.load_sample_data,
            style="Secondary.TButton"
        )
        self.sample_btn.grid(row=0, column=1, padx=(0, 15))
        
        # View reports folder button
        self.view_reports_btn = ttk.Button(
            left_frame,
            text="View Reports Folder",
            command=self.view_reports_folder,
            style="Secondary.TButton"
        )
        self.view_reports_btn.grid(row=0, column=2)
        
        # Right side - Generate report button (emphasized)
        self.generate_btn = ttk.Button(
            button_frame,
            text="🎓 Generate PDF Report",
            command=self.generate_report,
            state="disabled",
            style="Accent.TButton"
        )
        self.generate_btn.grid(row=0, column=1, sticky=tk.E, padx=(15, 0))
    
    def auto_size_window(self):
        """Automatically size the main window to fit content"""
        # Update all widgets to get proper sizing
        self.root.update_idletasks()
        
        # Get the required size based on content
        req_width = self.root.winfo_reqwidth()
        req_height = self.root.winfo_reqheight()
        
        # Set reasonable minimum and maximum sizes - optimized for content visibility
        min_width = 1300  # Increased minimum width
        min_height = 900  # Increased minimum height
        max_width = 1600
        max_height = 1100
        
        # Use appropriate size within bounds - with more padding
        width = max(min_width, min(req_width + 150, max_width))  # Extra padding
        height = max(min_height, min(req_height + 150, max_height))  # Extra padding
        
        # Center on screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        # Set the geometry with larger default size
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.minsize(min_width, min_height)
    
    def on_subject_selected(self, event=None):
        """Handle subject selection event"""
        selected_subject = self.subject_var.get()
        if selected_subject:
            coefficient = get_subject_coefficient(selected_subject)
            self.coefficient_var.set(f"{coefficient}")
            self.update_add_button_state()
    
    def on_score_changed(self, *args):
        """Handle score change event"""
        try:
            score = float(self.score_var.get())
            if 0 <= score <= 100:
                grade = self.calculator.score_to_grade(score)
                self.grade_var.set(grade)
            else:
                self.grade_var.set("Invalid range")
        except ValueError:
            self.grade_var.set("Enter score")
        
        self.update_add_button_state()
    
    def update_add_button_state(self):
        """Update the state of the add subject button"""
        subject = self.subject_var.get()
        score_text = self.score_var.get()
        
        # Check if subject is selected and not already added
        subject_valid = subject and subject not in [s['name'] for s in self.selected_subjects]
        
        # Check if score is valid
        score_valid = False
        try:
            score = float(score_text)
            score_valid = 0 <= score <= 100
        except ValueError:
            pass
        
        # Enable button if both conditions are met
        if subject_valid and score_valid:
            self.add_subject_btn.configure(state="normal")
        else:
            self.add_subject_btn.configure(state="disabled")
    
    def add_subject(self):
        """Add selected subject to the grades list"""
        subject_name = self.subject_var.get()
        score = float(self.score_var.get())
        coefficient = get_subject_coefficient(subject_name)
        grade = self.calculator.score_to_grade(score)
        weighted_score = score * coefficient
        comment = self.comment_text.get("1.0", tk.END).strip()
        
        # Create subject data
        subject_data = {
            'name': subject_name,
            'coefficient': coefficient,
            'score': score,
            'grade': grade,
            'weighted_score': weighted_score,
            'comment': comment or "No comment provided"
        }
        
        # Add to list and tree
        self.selected_subjects.append(subject_data)
        self.add_subject_to_tree(subject_data)
        
        # Clear inputs
        self.subject_var.set("")
        self.score_var.set("")
        self.coefficient_var.set("Select a subject")
        self.grade_var.set("Enter score")
        self.comment_text.delete("1.0", tk.END)
        
        # Update final grade
        self.update_final_grade()
        self.update_add_button_state()
        self.update_generate_button_state()
    
    def add_subject_to_tree(self, subject_data):
        """Add subject to the treeview"""
        comment_preview = subject_data['comment'][:50] + "..." if len(subject_data['comment']) > 50 else subject_data['comment']
        
        self.grades_tree.insert('', 'end', values=(
            subject_data['name'],
            f"{subject_data['coefficient']:.1f}",
            f"{subject_data['score']:.1f}",
            subject_data['grade'],
            f"{subject_data['weighted_score']:.2f}",
            comment_preview
        ))
    
    def on_subject_tree_select(self, event=None):
        """Handle tree selection event"""
        selection = self.grades_tree.selection()
        if selection:
            self.remove_subject_btn.configure(state="normal")
            self.edit_subject_btn.configure(state="normal")
        else:
            self.remove_subject_btn.configure(state="disabled")
            self.edit_subject_btn.configure(state="disabled")
    
    def generate_new_candidate_number(self):
        """Generate a new candidate number"""
        new_number = generate_candidate_number()
        self.candidate_number_var.set(new_number)
    
    def show_settings(self):
        """Show the settings dialog"""
        result = show_settings_dialog(self.root)
        if result:
            # Refresh the subject dropdown to reflect any changes
            current_selection = self.subject_var.get()
            self.subject_combo['values'] = get_subject_names()
            
            # Update coefficient display if a subject is currently selected
            if current_selection:
                self.on_subject_selected()
                
            messagebox.showinfo("Settings Updated", "Settings have been applied successfully!")
    
    def edit_subject(self):
        """Edit the selected subject"""
        selection = self.grades_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a subject to edit.")
            return
        
        # Get the selected item
        item = selection[0]
        index = self.grades_tree.index(item)
        subject_data = self.selected_subjects[index]
        
        # Create edit dialog
        edit_dialog = SubjectEditDialog(self.root, subject_data)
        result = edit_dialog.show()
        
        if result:
            # Update the subject data
            updated_data = edit_dialog.get_data()
            self.selected_subjects[index] = updated_data
            
            # Update the tree view
            self.grades_tree.item(item, values=(
                updated_data['name'],
                f"{updated_data['coefficient']:.1f}",
                f"{updated_data['score']:.1f}",
                updated_data['grade'],
                f"{updated_data['weighted_score']:.2f}",
                updated_data['comment'][:50] + "..." if len(updated_data['comment']) > 50 else updated_data['comment']
            ))
            
            # Update final grade
            self.update_final_grade()
            
            messagebox.showinfo("Subject Updated", f"Subject '{updated_data['name']}' has been updated successfully!")
    
    def remove_subject(self):
        """Remove selected subject from the list"""
        selection = self.grades_tree.selection()
        if selection:
            item = selection[0]
            index = self.grades_tree.index(item)
            
            # Remove from data and tree
            self.selected_subjects.pop(index)
            self.grades_tree.delete(item)
            
            # Update final grade
            self.update_final_grade()
            self.update_generate_button_state()
            self.remove_subject_btn.configure(state="disabled")
    
    def update_final_grade(self):
        """Update the final grade calculation"""
        if not self.selected_subjects:
            self.total_weighted_var.set("0.00")
            self.total_coefficient_var.set("0.00")
            self.weighted_average_var.set("0.00%")
            self.final_grade_var.set("N/A")
            return
        
        # Calculate final grade
        final_result = self.calculator.calculate_final_grade(self.selected_subjects)
        
        # Calculate totals
        total_weighted = sum(s['weighted_score'] for s in self.selected_subjects)
        total_coefficient = sum(s['coefficient'] for s in self.selected_subjects)
        
        # Update display
        self.total_weighted_var.set(f"{total_weighted:.2f}")
        self.total_coefficient_var.set(f"{total_coefficient:.2f}")
        self.weighted_average_var.set(f"{final_result['weighted_average']:.2f}%")
        self.final_grade_var.set(final_result['final_grade'])
    
    def update_generate_button_state(self):
        """Update the state of the generate report button"""
        # Enable if we have student name and at least one subject
        student_name = self.student_name_var.get().strip()
        has_subjects = len(self.selected_subjects) > 0
        
        if student_name and has_subjects:
            self.generate_btn.configure(state="normal")
        else:
            self.generate_btn.configure(state="disabled")
    
    def generate_report(self):
        """Generate the PDF report"""
        try:
            # Prepare student data
            final_result = self.calculator.calculate_final_grade(self.selected_subjects)
            total_weighted = sum(s['weighted_score'] for s in self.selected_subjects)
            total_coefficient = sum(s['coefficient'] for s in self.selected_subjects)
            
            student_data = {
                'name': self.student_name_var.get().strip(),
                'candidate_number': self.candidate_number_var.get().strip(),
                'exam_session': self.exam_session_var.get().strip(),
                'school': self.school_var.get().strip(),
                'subjects': self.selected_subjects,
                'final_grade': {
                    'total_weighted_score': total_weighted,
                    'total_coefficient': total_coefficient,
                    'weighted_average': final_result['weighted_average'],
                    'final_grade': final_result['final_grade']
                }
            }
            
            # Generate PDF
            filepath = self.pdf_generator.generate_report(student_data)
            
            # Show success message
            messagebox.showinfo(
                "Success",
                f"Report generated successfully!\\n\\nFile saved as:\\n{filepath}\\n\\nWould you like to open the reports folder?",
            )
            
            # Ask if user wants to open the folder
            if messagebox.askyesno("Open Folder", "Would you like to open the reports folder?"):
                self.view_reports_folder()
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report:\\n{str(e)}")
    
    def clear_all_data(self):
        """Clear all entered data"""
        if messagebox.askyesno("Confirm Clear", "Are you sure you want to clear all data?"):
            # Clear student info
            self.student_name_var.set("")
            self.candidate_number_var.set("")
            self.exam_session_var.set(f"June {datetime.now().year}")
            self.school_var.set(APP_SETTINGS['default_school'])
            
            # Clear subject selection
            self.subject_var.set("")
            self.score_var.set("")
            self.coefficient_var.set("Select a subject")
            self.grade_var.set("Enter score")
            self.comment_text.delete("1.0", tk.END)
            
            # Clear subjects list
            self.selected_subjects.clear()
            for item in self.grades_tree.get_children():
                self.grades_tree.delete(item)
            
            # Update final grade
            self.update_final_grade()
            self.update_add_button_state()
            self.update_generate_button_state()
    
    def load_sample_data(self):
        """Load sample data for testing"""
        # Clear existing data first
        self.clear_all_data()
        
        # Set student info
        self.student_name_var.set("John Smith")
        self.candidate_number_var.set("CB123456")
        self.exam_session_var.set("June 2024")
        self.school_var.set("Cambridge International School")
        
        # Sample subjects data
        sample_subjects = [
            {"name": "Mathematics", "score": 85, "comment": "Excellent problem-solving skills and strong understanding of algebraic concepts."},
            {"name": "Physics", "score": 78, "comment": "Good grasp of fundamental principles. Needs improvement in practical applications."},
            {"name": "English Literature", "score": 92, "comment": "Outstanding analytical skills and excellent written expression."},
            {"name": "Biology", "score": 88, "comment": "Strong understanding of biological processes and excellent laboratory skills."}
        ]
        
        # Add sample subjects
        for subject_info in sample_subjects:
            coefficient = get_subject_coefficient(subject_info["name"])
            grade = self.calculator.score_to_grade(subject_info["score"])
            weighted_score = subject_info["score"] * coefficient
            
            subject_data = {
                'name': subject_info["name"],
                'coefficient': coefficient,
                'score': subject_info["score"],
                'grade': grade,
                'weighted_score': weighted_score,
                'comment': subject_info["comment"]
            }
            
            self.selected_subjects.append(subject_data)
            self.add_subject_to_tree(subject_data)
        
        # Update final grade and buttons
        self.update_final_grade()
        self.update_generate_button_state()
        
        messagebox.showinfo("Sample Data Loaded", "Sample student data has been loaded successfully!")
    
    def view_reports_folder(self):
        """Open the reports folder in file explorer"""
        reports_path = os.path.abspath(APP_SETTINGS['report_folder'])
        
        # Create folder if it doesn't exist
        if not os.path.exists(reports_path):
            os.makedirs(reports_path)
        
        # Open folder based on OS
        import subprocess
        import sys
        
        try:
            if sys.platform == "win32":
                os.startfile(reports_path)
            elif sys.platform == "darwin":  # macOS
                subprocess.run(["open", reports_path])
            else:  # Linux
                subprocess.run(["xdg-open", reports_path])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open reports folder:\\n{str(e)}")

def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = CambridgeReportGUI(root)
    
    # Bind window close event
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()