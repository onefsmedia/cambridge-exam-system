#!/usr/bin/env python3
"""
Test script to generate a PDF matching Joe's template exactly with Teacher Comments
"""

from pdf_generator import CambridgePDFGenerator
import os

# Test data matching Joe's template structure with dynamic fields
test_data = {
    'student_name': 'Joe',
    'school_name': 'DOBEDA INTERNATIONAL SCHOOL',
    'centre_number': '12345',
    'candidate_number': '0001',
    'session': 'June 2024',
    'subjects': [
        {
            'name': 'Additional Mathematics',
            'coefficient': 1.3,
            'score': 86.0,
            'grade': 'A',
            'weighted_score': 111.8,
            'teacher_comments': 'Good'
        },
        {
            'name': 'Mathematics (A Level)',
            'coefficient': 1.5,
            'score': 77.0,
            'grade': 'B',
            'weighted_score': 115.5,
            'teacher_comments': 'Good'
        }
    ]
}

def test_joe_template():
    """Test the PDF generation with Joe's template data"""
    print("Testing PDF generation with Joe's template structure...")
    print(f"Current working directory: {os.getcwd()}")
    
    # Create PDF generator
    pdf_gen = CambridgePDFGenerator()
    
    # Generate PDF
    output_path = os.path.join(os.getcwd(), "test_joe_template.pdf")
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
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_joe_template()