#!/usr/bin/env python3
"""
Test script to generate a compact PDF with the updated font sizes and spacing
"""

from pdf_generator import CambridgePDFGenerator
import os

# Test data with 2 subjects to see if it fits on one page
test_data = {
    'student_name': 'John Smith',
    'session': 'June 2024',
    'subjects': [
        {
            'code': '4037',
            'name': 'Additional Mathematics',
            'score': 85,
            'grade': 'A',
            'coefficient': 1.5,
            'weighted_score': 127.5,
            'teacher_comments': 'Excellent performance in advanced mathematical concepts'
        },
        {
            'code': '0580',
            'name': 'Mathematics (Core)',
            'score': 92,
            'grade': 'A*',
            'coefficient': 1.0,
            'weighted_score': 92.0,
            'teacher_comments': 'Outstanding work in problem solving and mathematical reasoning'
        }
    ]
}

def test_compact_pdf():
    """Test the compact PDF generation"""
    print("Testing compact PDF generation...")
    print(f"Current working directory: {os.getcwd()}")
    
    # Create PDF generator
    pdf_gen = CambridgePDFGenerator()
    
    # Generate PDF
    output_path = os.path.join(os.getcwd(), "test_compact_report_v3.pdf")
    print(f"Output path: {output_path}")
    try:
        pdf_gen.generate_enhanced_report(test_data, output_path)
        
        print(f"✅ PDF generated successfully: {output_path}")
        
        # Check file size
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"📄 File size: {file_size} bytes")
        
        # Open PDF if possible
        if os.name == 'nt':  # Windows
            os.startfile(output_path)
        else:
            os.system(f"open {output_path}")
            
    except Exception as e:
        print(f"❌ Error generating PDF: {e}")

if __name__ == "__main__":
    test_compact_pdf()