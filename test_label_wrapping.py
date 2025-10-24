#!/usr/bin/env python3
"""
Test CustomTkinter label text wrapping behavior
"""
import customtkinter as ctk

def wrap_text(text, max_length=16):
    """Enhanced text wrapping function"""
    if len(text) <= max_length:
        return text
    
    # For very long subject names, use more aggressive wrapping
    if len(text) > 25:
        max_length = 12
    
    words = text.split()
    lines = []
    current_line = ""
    
    for word in words:
        test_line = current_line + (" " + word if current_line else word)
        
        if len(test_line) <= max_length:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
                current_line = word
                if len(current_line) > max_length:
                    lines.append(current_line[:max_length-3] + "...")
                    current_line = ""
            else:
                lines.append(word[:max_length-3] + "...")
                current_line = ""
    
    if current_line:
        lines.append(current_line)
    
    return "\n".join(lines)

def test_label_wrapping():
    """Test label wrapping with various configurations"""
    app = ctk.CTk()
    app.title("Text Wrapping Test")
    app.geometry("800x600")
    
    # Configure grid
    app.grid_columnconfigure(0, weight=0, minsize=150)
    app.grid_columnconfigure(1, weight=0, minsize=150)
    app.grid_columnconfigure(2, weight=1)
    
    test_subjects = [
        ("0654", "Co-ordinated Sciences (Double Award)"),
        ("0522", "First Language English (US)"),
        ("9695", "Literature in English (A Level)"),
        ("9709", "Mathematics (A Level)"),
        ("0606", "Additional Mathematics")
    ]
    
    # Headers
    headers = ["Subject Code", "Subject Name", "Wrapped Display"]
    for i, header in enumerate(headers):
        label = ctk.CTkLabel(app, text=header, font=ctk.CTkFont(size=14, weight="bold"))
        label.grid(row=0, column=i, padx=10, pady=10, sticky="w")
    
    # Test each subject
    for row, (code, name) in enumerate(test_subjects, 1):
        # Code
        code_label = ctk.CTkLabel(app, text=code, width=100)
        code_label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
        
        # Original name
        name_label = ctk.CTkLabel(app, text=name, width=200)
        name_label.grid(row=row, column=1, padx=10, pady=5, sticky="w")
        
        # Wrapped display
        wrapped = wrap_text(name, 16)
        display_text = f"{code}:\n{wrapped}"
        wrapped_label = ctk.CTkLabel(
            app, 
            text=display_text,
            font=ctk.CTkFont(size=10),
            justify="left",
            width=150,
            height=60,
            anchor="nw",
            wraplength=140
        )
        wrapped_label.grid(row=row, column=2, padx=10, pady=5, sticky="nw")
    
    app.mainloop()

if __name__ == "__main__":
    test_label_wrapping()