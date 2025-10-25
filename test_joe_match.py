#!/usr/bin/env python3
"""
Test script to generate a PDF matching Joe_Joe_cambridge_report.pdf exactly
"""

from pdf_generator import CambridgePDFGenerator
import os

# Test data matching Joe's template with teacher comments
test_data = {
    'student_name': 'Joe Joe',
    'session': 'June 2024',
    'subjects': [
        {
            'code': '9709',
            'name': 'Mathematics',
            'score': 95,
            'grade': 'A*',
            'grade_points': 4.0,
            'teacher_comments': 'Exceptional performance in all areas of mathematics. Shows strong analytical thinking and problem-solving skills. Consistently produces high-quality work and demonstrates deep understanding of advanced mathematical concepts.'
        },
        {
            'code': '9702',
            'name': 'Physics',
            'score': 89,
            'grade': 'A',
            'grade_points': 3.7,
            'teacher_comments': 'Excellent understanding of physics concepts with strong practical laboratory skills. Shows initiative in independent research and consistently applies theoretical knowledge to solve complex problems.'
        },
        {
            'code': '9701',
            'name': 'Chemistry',
            'score': 87,
            'grade': 'A',
            'grade_points': 3.7,
            'teacher_comments': 'Strong performance in both theoretical and practical chemistry. Well-organized approach to problem solving with good laboratory technique and accurate data analysis.'
        }
    ]
}

def test_joe_exact_match():
    """Test PDF generation to match Joe's template exactly"""
    print("Testing Joe template exact match...")
    print(f"Current working directory: {os.getcwd()}")
    
    # Create PDF generator
    pdf_gen = CambridgePDFGenerator()
    
    # Generate PDF
    output_path = os.path.join(os.getcwd(), "Joe_Joe_exact_match.pdf")
    print(f"Output path: {output_path}")
    
    try:
        pdf_gen.generate_enhanced_report(test_data, "Joe_Joe_exact_match.pdf")
        
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
    test_joe_exact_match()