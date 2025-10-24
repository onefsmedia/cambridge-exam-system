#!/usr/bin/env python3
"""
Test text wrapping functionality
"""

def wrap_text(text, max_length=16):
    """Wrap text to fit within specified length, optimized for UI display"""
    if len(text) <= max_length:
        return text
    
    # Find a good break point
    words = text.split()
    lines = []
    current_line = ""
    
    for word in words:
        # Check if adding this word would exceed the limit
        test_line = current_line + (" " + word if current_line else word)
        
        if len(test_line) <= max_length:
            current_line = test_line
        else:
            # If current line has content, save it and start new line
            if current_line:
                lines.append(current_line)
                current_line = word
            else:
                # Word itself is too long, truncate it
                lines.append(word[:max_length-3] + "...")
                current_line = ""
    
    if current_line:
        lines.append(current_line)
    
    return "\n".join(lines)

# Test with problematic subject names
test_subjects = [
    "Mathematics (A Level)",
    "Additional Mathematics", 
    "Co-ordinated Sciences (Double Award)",
    "First Language English (US)",
    "Literature in English (A Level)"
]

print("Text Wrapping Test Results:")
print("=" * 50)

for subject in test_subjects:
    wrapped = wrap_text(subject, 16)
    print(f"\nOriginal: {subject}")
    print(f"Wrapped:\n{wrapped}")
    print("-" * 30)