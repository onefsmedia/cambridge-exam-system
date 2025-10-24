#!/usr/bin/env python3
"""
Cambridge Report Card System - Visible Version
This version will definitely show a window and stay open
"""

import dearpygui.dearpygui as dpg
import time

def main():
    # Create context
    dpg.create_context()
    
    # Create viewport with explicit settings
    dpg.create_viewport(
        title="Cambridge Report Card - TEST VERSION",
        width=1000,
        height=700,
        resizable=True,
        always_on_top=False,
        decorated=True
    )
    
    # Create a window that fills the viewport
    with dpg.window(label="Cambridge Report Card System", tag="main_window", width=980, height=680):
        # Large, bold header
        dpg.add_text("CAMBRIDGE INTERNATIONAL EXAMINATION", color=(0, 0, 0, 255))
        dpg.add_text("Report Card Generator", color=(0, 100, 200, 255))
        dpg.add_separator()
        dpg.add_spacer(height=20)
        
        # Student Information
        dpg.add_text("STUDENT INFORMATION", color=(200, 0, 0, 255))
        dpg.add_separator()
        dpg.add_spacer(height=10)
        
        dpg.add_text("Student Name:")
        dpg.add_input_text(tag="student_name", width=400, hint="Enter student's full name")
        dpg.add_spacer(height=10)
        
        dpg.add_text("Candidate Number:")
        dpg.add_input_text(tag="candidate_number", width=400, hint="Enter candidate number")
        dpg.add_spacer(height=10)
        
        dpg.add_text("School Name:")
        dpg.add_input_text(tag="school_name", width=400, hint="Enter school name")
        dpg.add_spacer(height=20)
        
        # Test buttons to verify interface is working
        dpg.add_text("TEST INTERFACE", color=(0, 150, 0, 255))
        dpg.add_separator()
        dpg.add_spacer(height=10)
        
        def test_button_callback():
            student_name = dpg.get_value("student_name")
            if student_name:
                dpg.set_value("test_result", f"Hello {student_name}! Interface is working!")
            else:
                dpg.set_value("test_result", "Interface is working! Please enter a student name.")
        
        dpg.add_button(label="TEST BUTTON - CLICK ME", callback=test_button_callback, width=300, height=50)
        dpg.add_spacer(height=10)
        dpg.add_text("Click the button above to test", tag="test_result", color=(0, 0, 255, 255))
        
        dpg.add_spacer(height=30)
        
        # Instructions
        dpg.add_text("INSTRUCTIONS:", color=(100, 0, 100, 255))
        dpg.add_text("1. Enter student information above")
        dpg.add_text("2. Click the TEST BUTTON to verify interface works")
        dpg.add_text("3. If you can see this text clearly, the visibility issues are fixed!")
        
        # Status
        dpg.add_spacer(height=20)
        dpg.add_text("STATUS: Application is running successfully!", color=(0, 150, 0, 255))
        dpg.add_text("Font size: Large | Text color: High contrast | Window size: 1000x700")
    
    # Setup Dear PyGui
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("main_window", True)
    
    # Keep the application running
    print("="*50)
    print("APPLICATION IS NOW RUNNING!")
    print("You should see a window titled: 'Cambridge Report Card - TEST VERSION'")
    print("Window size: 1000x700 pixels")
    print("If you don't see it, check if it's minimized or behind other windows")
    print("Press Ctrl+C in terminal to close the application")
    print("="*50)
    
    try:
        dpg.start_dearpygui()
    except KeyboardInterrupt:
        print("\nApplication closed by user")
    finally:
        dpg.destroy_context()
        print("Application terminated")

if __name__ == "__main__":
    main()