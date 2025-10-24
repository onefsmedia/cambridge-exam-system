#!/usr/bin/env python3
"""
Simple test for Dear PyGui to verify installation and basic functionality
"""

import dearpygui.dearpygui as dpg

def main():
    # Create context
    dpg.create_context()
    
    # Create viewport
    dpg.create_viewport(
        title="Dear PyGui Test",
        width=800,
        height=600
    )
    
    # Create a simple window
    with dpg.window(label="Test Window", tag="main_window"):
        dpg.add_text("Hello, Dear PyGui!")
        dpg.add_button(label="Test Button", callback=lambda: print("Button clicked!"))
    
    # Setup and show
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("main_window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == "__main__":
    main()