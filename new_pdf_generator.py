"""
PDF Report Generator to match Joe_Joe_cambridge_report.pdf template exactly
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from datetime import datetime
import os

class JoeCambridgePDFGenerator:
    """Generate Cambridge-style report card PDFs matching Joe's template exactly"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom paragraph styles matching the template"""
        # Cambridge header title style
        self.styles.add(ParagraphStyle(
            name='CambridgeTitle',
            parent=self.styles['Normal'],
            fontSize=16,
            fontName='Helvetica-Bold',
            alignment=TA_CENTER,
            spaceAfter=8,
            textColor=colors.black
        ))
        
        # Cambridge subtitle style
        self.styles.add(ParagraphStyle(
            name='CambridgeSubtitle',
            parent=self.styles['Normal'],
            fontSize=12,
            fontName='Helvetica-Bold',
            alignment=TA_CENTER,
            spaceAfter=6,
            textColor=colors.black
        ))
        
        # Cambridge document type style
        self.styles.add(ParagraphStyle(
            name='CambridgeDocType',
            parent=self.styles['Normal'],
            fontSize=14,
            fontName='Helvetica-Bold',
            alignment=TA_CENTER,
            spaceAfter=20,
            textColor=colors.black
        ))
        
        # Body text style
        self.styles.add(ParagraphStyle(
            name='JoeBodyText',
            parent=self.styles['Normal'],
            fontSize=11,
            fontName='Helvetica',
            alignment=TA_LEFT,
            spaceAfter=6
        ))
        
        # Bold body text style
        self.styles.add(ParagraphStyle(
            name='JoeBodyTextBold',
            parent=self.styles['Normal'],
            fontSize=11,
            fontName='Helvetica-Bold',
            alignment=TA_LEFT,
            spaceAfter=6
        ))
        
        # Comments style
        self.styles.add(ParagraphStyle(
            name='JoeComments',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='Helvetica',
            alignment=TA_JUSTIFY,
            spaceAfter=4,
            leftIndent=10,
            rightIndent=10
        ))
        
        # Footer style
        self.styles.add(ParagraphStyle(
            name='JoeFooter',
            parent=self.styles['Normal'],
            fontSize=9,
            fontName='Helvetica',
            alignment=TA_CENTER,
            textColor=colors.grey
        ))

    def generate_joe_template_report(self, student_data, filename=None):
        """Generate a report matching Joe's template exactly"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            student_name = student_data.get('student_name', 'Student').replace(' ', '_')
            filename = f"{student_name}_cambridge_report_{timestamp}.pdf"
        
        # Ensure reports directory exists
        reports_dir = "reports"
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)
        
        filepath = os.path.join(reports_dir, filename)
        
        # Create PDF document with exact margins
        doc = SimpleDocTemplate(
            filepath,
            pagesize=A4,
            rightMargin=1*inch,
            leftMargin=1*inch,
            topMargin=0.8*inch,
            bottomMargin=1*inch
        )
        
        # Build content
        story = []
        
        # Header
        story.extend(self._create_cambridge_header())
        
        # Student information
        story.extend(self._create_student_info(student_data))
        
        # Grades table
        story.extend(self._create_grades_table(student_data))
        
        # Teacher comments section
        story.extend(self._create_comments_section(student_data))
        
        # Footer
        story.extend(self._create_footer())
        
        # Build PDF
        doc.build(story)
        
        return filepath

    def _create_cambridge_header(self):
        """Create the Cambridge International Examinations header"""
        content = []
        
        # Main Cambridge title
        cambridge_title = Paragraph("CAMBRIDGE INTERNATIONAL EXAMINATIONS", self.styles['CambridgeTitle'])
        content.append(cambridge_title)
        
        # Advanced Level subtitle
        advanced_level = Paragraph("General Certificate of Education Advanced Level", self.styles['CambridgeSubtitle'])
        content.append(advanced_level)
        
        # Statement of Results
        statement = Paragraph("STATEMENT OF RESULTS", self.styles['CambridgeDocType'])
        content.append(statement)
        
        content.append(Spacer(1, 15))
        
        return content

    def _create_student_info(self, student_data):
        """Create student information section"""
        content = []
        
        # Student info table data
        info_data = [
            ['Centre Number:', '12345', 'Session:', student_data.get('session', 'June 2024')],
            ['Candidate Name:', student_data.get('student_name', 'Unknown'), 'Candidate Number:', '0001'],
        ]
        
        # Create table
        info_table = Table(info_data, colWidths=[2.2*inch, 2.2*inch, 1.8*inch, 1.8*inch])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            # Bold the labels
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ]))
        
        content.append(info_table)
        content.append(Spacer(1, 20))
        
        return content

    def _create_grades_table(self, student_data):
        """Create the grades table matching Joe's template"""
        content = []
        
        # Table header
        headers = ['Subject Code', 'Subject Title', 'Grade', 'Score', 'Grade Points']
        
        # Prepare data
        table_data = [headers]
        
        total_points = 0
        total_subjects = 0
        
        # Add subject data
        for subject in student_data.get('subjects', []):
            row = [
                subject.get('code', ''),
                subject.get('name', ''),
                subject.get('grade', ''),
                str(subject.get('score', '')),
                str(subject.get('grade_points', subject.get('weighted_score', '')))
            ]
            table_data.append(row)
            
            # Calculate totals for GPA
            if 'grade_points' in subject:
                total_points += float(subject['grade_points'])
                total_subjects += 1
            elif 'weighted_score' in subject:
                total_points += float(subject['weighted_score'])
                total_subjects += 1
        
        # Calculate GPA
        gpa = total_points / total_subjects if total_subjects > 0 else 0
        
        # Add GPA row
        table_data.append(['', 'Overall GPA:', f"{gpa:.2f}", '', ''])
        
        # Create table
        grades_table = Table(table_data, colWidths=[1.2*inch, 3*inch, 0.8*inch, 0.8*inch, 1.2*inch])
        
        # Apply styling
        grades_table.setStyle(TableStyle([
            # Header row styling
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            
            # Data rows styling
            ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -2), 10),
            ('ALIGN', (0, 1), (0, -2), 'CENTER'),  # Subject codes
            ('ALIGN', (1, 1), (1, -2), 'LEFT'),    # Subject names
            ('ALIGN', (2, 1), (-1, -2), 'CENTER'), # Grades, scores, points
            
            # GPA row styling
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -1), (-1, -1), 11),
            ('ALIGN', (1, -1), (1, -1), 'RIGHT'),
            ('ALIGN', (2, -1), (2, -1), 'CENTER'),
            
            # Grid
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            
            # Padding
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        content.append(grades_table)
        content.append(Spacer(1, 20))
        
        return content

    def _create_comments_section(self, student_data):
        """Create teacher comments section"""
        content = []
        
        # Comments header
        comments_header = Paragraph("Teacher Comments:", self.styles['JoeBodyTextBold'])
        content.append(comments_header)
        content.append(Spacer(1, 10))
        
        # Add comments for each subject
        for subject in student_data.get('subjects', []):
            comment = subject.get('teacher_comments', '').strip()
            if comment:
                subject_name = subject.get('name', 'Unknown Subject')
                
                # Subject name in bold
                subject_para = Paragraph(f"<b>{subject_name}:</b>", self.styles['JoeBodyText'])
                content.append(subject_para)
                
                # Comment text
                comment_para = Paragraph(comment, self.styles['JoeComments'])
                content.append(comment_para)
                content.append(Spacer(1, 8))
        
        content.append(Spacer(1, 20))
        return content

    def _create_footer(self):
        """Create footer with DOBEDA copyright"""
        content = []
        
        # Add significant space before footer
        content.append(Spacer(1, 40))
        
        # Signature lines
        sig_data = [
            ['Principal/Head Teacher:', '_' * 30, 'Date:', '_' * 20],
        ]
        
        sig_table = Table(sig_data, colWidths=[2*inch, 2*inch, 1*inch, 1.5*inch])
        sig_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('ALIGN', (2, 0), (2, -1), 'LEFT'),
            ('ALIGN', (3, 0), (3, -1), 'CENTER'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        
        content.append(sig_table)
        content.append(Spacer(1, 30))
        
        # DOBEDA copyright footer
        footer_text = Paragraph("© 2024 DOBEDA - Cambridge Examination Report System", self.styles['JoeFooter'])
        content.append(footer_text)
        
        return content

# Test function
def test_joe_template():
    """Test the new template generator"""
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
                'teacher_comments': 'Exceptional performance in all areas of mathematics. Shows strong analytical thinking and problem-solving skills. Consistently produces high-quality work.'
            },
            {
                'code': '9702',
                'name': 'Physics',
                'score': 89,
                'grade': 'A',
                'grade_points': 3.7,
                'teacher_comments': 'Excellent understanding of physics concepts. Good practical skills in laboratory work. Shows initiative in independent research.'
            },
            {
                'code': '9701',
                'name': 'Chemistry',
                'score': 87,
                'grade': 'A',
                'grade_points': 3.7,
                'teacher_comments': 'Strong performance in both theoretical and practical chemistry. Well-organized approach to problem solving.'
            }
        ]
    }
    
    # Create generator and generate report
    generator = JoeCambridgePDFGenerator()
    output_path = generator.generate_joe_template_report(test_data, "Joe_Joe_template_match.pdf")
    
    print(f"✅ Joe template PDF generated: {output_path}")
    
    # Open PDF if on Windows
    if os.name == 'nt':
        os.startfile(output_path)

if __name__ == "__main__":
    test_joe_template()