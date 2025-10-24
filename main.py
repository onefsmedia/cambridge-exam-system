"""
Cambridge Exam Report Card Generator
Main application entry point

This application generates professional Cambridge-style exam report cards
with weighted grades, teacher comments, and PDF output.

Features:
- Subject selection with automatic coefficient display
- Grade calculation using Cambridge grading system
- Teacher comments for each subject
- Final weighted grade calculation
- Professional PDF report generation
- Cross-platform GUI using tkinter

Author: Cambridge Report System
Version: 1.0.0
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    from main_gui import CambridgeReportGUI
    from config import APP_SETTINGS
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Please ensure all required files are in the same directory.")
    sys.exit(1)

def check_dependencies():
    """Check if all required dependencies are available"""
    missing_modules = []
    
    # Check for reportlab
    try:
        import reportlab
    except ImportError:
        missing_modules.append("reportlab")
    
    # Check for tkinter (should be built-in)
    try:
        import tkinter
    except ImportError:
        missing_modules.append("tkinter")
    
    return missing_modules

def show_welcome_message():
    """Show welcome message with application information"""
    welcome_text = f"""
Welcome to {APP_SETTINGS['title']}!

This application helps you generate professional Cambridge International 
Examination report cards with the following features:

• Subject selection with Cambridge coefficients
• Automatic grade calculation (A* to G scale)
• Teacher comments for each subject
• Final weighted grade calculation
• Professional PDF report generation

To get started:
1. Enter student information
2. Select subjects and enter scores
3. Add teacher comments
4. Generate your PDF report

Version: {APP_SETTINGS['version']}
    """
    
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    
    messagebox.showinfo("Welcome", welcome_text.strip())
    root.destroy()

def main():
    """Main application function"""
    print(f"Starting {APP_SETTINGS['title']} v{APP_SETTINGS['version']}")
    print("=" * 60)
    
    # Check dependencies
    missing_modules = check_dependencies()
    if missing_modules:
        error_msg = f"""
Missing required dependencies: {', '.join(missing_modules)}

To install missing dependencies, run:
pip install {' '.join(missing_modules)}

For a complete installation, run:
pip install -r requirements.txt
"""
        print(error_msg)
        
        # Try to show GUI error message
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Missing Dependencies", error_msg)
            root.destroy()
        except:
            pass
        
        return 1
    
    try:
        # Show welcome message
        show_welcome_message()
        
        # Create and run the main application
        root = tk.Tk()
        app = CambridgeReportGUI(root)
        
        print("Application started successfully!")
        print("GUI window should now be visible.")
        print("Close this terminal window or press Ctrl+C to exit.")
        
        # Start the GUI event loop
        root.mainloop()
        
        print("Application closed successfully.")
        return 0
        
    except KeyboardInterrupt:
        print("\\nApplication interrupted by user.")
        return 0
        
    except Exception as e:
        error_msg = f"An error occurred while starting the application:\\n{str(e)}"
        print(f"ERROR: {error_msg}")
        
        # Try to show GUI error message
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Application Error", error_msg)
            root.destroy()
        except:
            pass
        
        return 1

if __name__ == "__main__":
    # Set up proper error handling for Windows
    if sys.platform == "win32":
        try:
            sys.exit(main())
        except Exception as e:
            print(f"Fatal error: {e}")
            input("Press Enter to exit...")
            sys.exit(1)
    else:
        sys.exit(main())