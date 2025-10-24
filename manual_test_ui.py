"""
Manual test for checking if the UI sizing issues are resolved
"""

import tkinter as tk
import sys
import os

# Add the cambridge_report_system to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main_gui import CambridgeReportGUI

def test_ui_display():
    """Test the UI display by launching the application"""
    print("Cambridge Report Card Generator - UI Display Test")
    print("=" * 60)
    print("\nInstructions:")
    print("1. The main window should display properly with all sections visible")
    print("2. Click the 'Settings' button to test the settings dialog")
    print("3. The settings dialog should show all content without requiring manual resize")
    print("4. Add a subject and try 'Edit Subject' to test that dialog")
    print("5. Close the application when testing is complete")
    print("\nStarting application...")
    
    root = tk.Tk()
    app = CambridgeReportGUI(root)
    
    # Add some sample data to test edit functionality
    app.subject_var.set("Mathematics")
    app.score_var.set("85")
    app.on_subject_selected()
    
    print("Application is ready for testing!")
    print("Main window dimensions:", root.geometry())
    
    root.mainloop()

if __name__ == "__main__":
    test_ui_display()