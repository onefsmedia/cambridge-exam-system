#!/usr/bin/env python3
"""
Test CustomTkinter wraplength parameter for text wrapping
"""
import customtkinter as ctk

def test_wraplength_wrapping():
    """Test that CustomTkinter wraplength works correctly"""
    app = ctk.CTk()
    app.title("CustomTkinter Wrapping Test")
    app.geometry("600x400")
    
    # Configure grid
    app.grid_columnconfigure(0, weight=0, minsize=150)
    app.grid_columnconfigure(1, weight=1)
    
    test_subjects = [
        ("0654", "Co-ordinated Sciences (Double Award)"),
        ("0522", "First Language English (US)"),
        ("9695", "Literature in English (A Level)"),
        ("9709", "Mathematics (A Level)"),
        ("0606", "Additional Mathematics")
    ]
    
    # Header
    header = ctk.CTkLabel(app, text="Subject Display Test with wraplength", 
                         font=ctk.CTkFont(size=16, weight="bold"))
    header.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
    
    # Test each subject
    for row, (code, name) in enumerate(test_subjects, 1):
        # Subject display using wraplength (no manual \n breaks)
        subject_display = f"{code}: {name}"
        
        wrapped_label = ctk.CTkLabel(
            app, 
            text=subject_display,
            font=ctk.CTkFont(size=10),
            justify="left",
            width=150,
            height=60,
            anchor="nw",
            wraplength=140  # CustomTkinter handles wrapping automatically
        )
        wrapped_label.grid(row=row, column=0, padx=10, pady=5, sticky="nw")
        
        # Info label
        info_text = f"Original: '{name}' ({len(name)} chars)\nwraplength=140, width=150"
        info_label = ctk.CTkLabel(app, text=info_text, justify="left")
        info_label.grid(row=row, column=1, padx=10, pady=5, sticky="w")
    
    # Add note
    note = ctk.CTkLabel(
        app, 
        text="Note: Text wrapping is handled by CustomTkinter's wraplength parameter.\nNo manual \\n characters are inserted into the text.",
        font=ctk.CTkFont(size=12),
        justify="center",
        text_color=("gray60", "gray40")
    )
    note.grid(row=len(test_subjects)+1, column=0, columnspan=2, padx=10, pady=20)
    
    app.mainloop()

if __name__ == "__main__":
    test_wraplength_wrapping()