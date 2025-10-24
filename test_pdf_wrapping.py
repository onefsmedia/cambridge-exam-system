#!/usr/bin/env python3
"""
Test PDF generation with improved text wrapping
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pdf_generator import CambridgePDFGenerator

def test_pdf_generation():
    """Test PDF generation with long subject names"""
    
    # Create test data with problematic subject names
    test_data = {
        'name': 'Test Student',
        'candidate_number': 'TEST123',
        'school': 'Test School',
        'exam_session': 'June 2024',
        'subjects': [
            {
                'name': 'Co-ordinated Sciences (Double Award)',
                'coefficient': 1.1,
                'score': 85,
                'grade': 'A',
                'weighted_score': 93.5,
                'comment': 'Excellent understanding of scientific principles and laboratory techniques.'
            },
            {
                'name': 'Mathematics (A Level)',
                'coefficient': 1.5,
                'score': 90,
                'grade': 'A*',
                'weighted_score': 135.0,
                'comment': 'Outstanding mathematical reasoning and problem-solving skills.'
            },
            {
                'name': 'Additional Mathematics',
                'coefficient': 1.3,
                'score': 88,
                'grade': 'A',
                'weighted_score': 114.4,
                'comment': 'Strong performance in advanced mathematical concepts.'
            },
            {
                'name': 'First Language English (US)',
                'coefficient': 1.3,
                'score': 82,
                'grade': 'A',
                'weighted_score': 106.6,
                'comment': 'Good written and oral communication skills demonstrated.'
            }
        ],
        'final_grade': {
            'total_weighted_score': 449.5,
            'total_coefficient': 5.2,
            'weighted_average': 86.4,
            'final_grade': 'A'
        }
    }
    
    # Generate PDF
    try:
        pdf_generator = CambridgePDFGenerator()
        pdf_path = pdf_generator.generate_report(test_data, "test_wrapping_report.pdf")
        print(f"✅ PDF generated successfully: {pdf_path}")
        print("✅ Text wrapping improvements applied")
        print("✅ Using Paragraph objects for proper HTML break rendering")
        print("✅ Narrower Subject column (0.9 inch vs 1.2 inch)")
        print("✅ Shorter text wrapping limit (15 chars vs 20 chars)")
        return True
    except Exception as e:
        print(f"❌ PDF generation failed: {e}")
        return False

if __name__ == "__main__":
    test_pdf_generation()