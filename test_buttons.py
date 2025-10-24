#!/usr/bin/env python3
"""
Test script to verify PDF and Email button functionality
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from main_gui_complete import ComprehensiveCambridgeGUI
    import customtkinter as ctk
    
    # Create the app
    print("Creating application...")
    app = ComprehensiveCambridgeGUI()
    
    # Test basic functionality
    print("Testing basic initialization...")
    print(f"Selected subjects: {app.selected_subjects}")
    print(f"PDF generator available: {app.pdf_generator is not None}")
    
    # Test if we can manually trigger methods
    print("\nTesting manual method calls...")
    
    # Try to call the PDF generation with no data (should show warning)
    print("Calling generate_comprehensive_pdf with no data...")
    try:
        app.generate_comprehensive_pdf()
        print("PDF method called successfully")
    except Exception as e:
        print(f"PDF method error: {e}")
    
    # Try to call email function
    print("Calling email_report with no data...")
    try:
        app.email_report()
        print("Email method called successfully")
    except Exception as e:
        print(f"Email method error: {e}")
    
    print("\nTest completed - if you see warning dialogs, the buttons are working!")
    print("The app window should be visible. Try clicking the buttons manually.")
    
    # Run the app
    app.run()
    
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure all dependencies are installed:")
    print("pip install customtkinter reportlab")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()