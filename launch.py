#!/usr/bin/env python3
"""
Cambridge Report Card Generator Launcher
This script ensures the GUI launches with proper error handling
"""

import sys
import os
import traceback

# Ensure we can find our modules
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

def main():
    """Main launcher function"""
    try:
        # Import required modules
        import tkinter as tk
        from main_gui import CambridgeReportGUI
        from config import APP_SETTINGS
        
        print(f"Starting {APP_SETTINGS['title']} v{APP_SETTINGS['version']}")
        print("=" * 60)
        print("NEW FEATURES ADDED:")
        print("* Auto-generated candidate numbers (CB + Year + Random)")
        print("* Settings dialog for modifying subject coefficients")
        print("* Edit subject functionality with dedicated dialog")
        print("* Repositioned Generate Report button (bottom right)")
        print("* Enhanced GUI layout and user experience")
        print("=" * 60)
        
        # Create and run the application
        root = tk.Tk()
        app = CambridgeReportGUI(root)
        
        print("Application window should now be visible.")
        print("New features available:")
        print("- Automatic candidate number generation")
        print("- Settings button for coefficient management")
        print("- Edit Selected Subject button")
        print("- Generate PDF Report button (bottom right)")
        print("You can close this console window once the GUI opens.")
        
        # Start the GUI
        root.mainloop()
        
        print("Application closed successfully.")
        
    except ImportError as e:
        error_msg = f"""
IMPORT ERROR: {e}

This usually means reportlab is not installed.
Please run: pip install reportlab

Or install all requirements: pip install -r requirements.txt
"""
        print(error_msg)
        
        # Try to show a GUI error message
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Missing Dependencies", error_msg)
            root.destroy()
        except:
            pass
            
        input("Press Enter to exit...")
        return 1
        
    except Exception as e:
        error_msg = f"""
UNEXPECTED ERROR: {e}

{traceback.format_exc()}
"""
        print(error_msg)
        
        # Try to show a GUI error message
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Application Error", f"An error occurred: {e}")
            root.destroy()
        except:
            pass
            
        input("Press Enter to exit...")
        return 1

if __name__ == "__main__":
    sys.exit(main())