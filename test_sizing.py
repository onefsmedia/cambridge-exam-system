"""
Test script to verify window auto-sizing functionality
"""

import tkinter as tk
import sys
import os

# Add the cambridge_report_system to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main_gui import CambridgeReportGUI
from settings_dialog import SettingsDialog

def test_main_window_sizing():
    """Test main window auto-sizing"""
    print("Testing main window auto-sizing...")
    
    root = tk.Tk()
    app = CambridgeReportGUI(root)
    
    # Update to get actual dimensions
    root.update_idletasks()
    
    # Get window dimensions
    width = root.winfo_width()
    height = root.winfo_height()
    req_width = root.winfo_reqwidth()
    req_height = root.winfo_reqheight()
    
    print(f"Main window dimensions: {width}x{height}")
    print(f"Required dimensions: {req_width}x{req_height}")
    print(f"Window geometry: {root.geometry()}")
    
    # Check if window is properly sized
    if width >= 1050 and height >= 750:
        print("✓ Main window sizing: PASSED")
    else:
        print("✗ Main window sizing: FAILED")
    
    root.destroy()
    return width >= 1050 and height >= 750

def test_settings_dialog_sizing():
    """Test settings dialog auto-sizing"""
    print("\nTesting settings dialog auto-sizing...")
    
    root = tk.Tk()
    root.withdraw()  # Hide main window
    
    # Create settings dialog
    dialog = SettingsDialog(root)
    
    # Wait for delayed sizing to complete
    root.update()
    root.after(50, lambda: None)  # Wait for delayed sizing
    root.update()
    
    # Update multiple times to ensure complete layout
    for _ in range(3):
        dialog.dialog.update_idletasks()
        root.update()
    
    # Get dialog dimensions
    width = dialog.dialog.winfo_width()
    height = dialog.dialog.winfo_height()
    req_width = dialog.dialog.winfo_reqwidth()
    req_height = dialog.dialog.winfo_reqheight()
    
    print(f"Settings dialog dimensions: {width}x{height}")
    print(f"Required dimensions: {req_width}x{req_height}")
    print(f"Dialog geometry: {dialog.dialog.geometry()}")
    
    # Check if dialog is properly sized
    if width >= 650 and height >= 550:
        print("✓ Settings dialog sizing: PASSED")
        result = True
    else:
        print("✗ Settings dialog sizing: FAILED")
        result = False
    
    dialog.dialog.destroy()
    root.destroy()
    return result

if __name__ == "__main__":
    print("Cambridge Report Card Generator - Window Sizing Test")
    print("=" * 60)
    
    try:
        main_test = test_main_window_sizing()
        settings_test = test_settings_dialog_sizing()
        
        print("\n" + "=" * 60)
        print("Test Summary:")
        print(f"Main window auto-sizing: {'PASSED' if main_test else 'FAILED'}")
        print(f"Settings dialog auto-sizing: {'PASSED' if settings_test else 'FAILED'}")
        
        if main_test and settings_test:
            print("\n🎉 All window sizing tests PASSED!")
            print("The UI display issue should now be resolved.")
        else:
            print("\n❌ Some tests FAILED. Further adjustments may be needed.")
            
    except Exception as e:
        print(f"Test failed with error: {e}")
        import traceback
        traceback.print_exc()