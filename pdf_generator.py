"""
PDF Report Generator for Cambridge Exam Report Cards
Uses reportlab to create professional-looking PDF reports
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import os
from config import PDF_STYLE, APP_SETTINGS

class CambridgePDFGenerator:
    """Generate Cambridge-style report card PDFs"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom paragraph styles for the report"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=PDF_STYLE['title_font_size'],
            alignment=TA_CENTER,
            spaceAfter=30,
            textColor=colors.darkblue
        ))
        
        # Header style
        self.styles.add(ParagraphStyle(
            name='CustomHeader',
            parent=self.styles['Heading2'],
            fontSize=PDF_STYLE['header_font_size'],
            alignment=TA_CENTER,
            spaceAfter=20
        ))
        
        # Body style
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=PDF_STYLE['body_font_size'],
            alignment=TA_LEFT,
            spaceAfter=12
        ))
        
        # Small text style
        self.styles.add(ParagraphStyle(
            name='CustomSmall',
            parent=self.styles['Normal'],
            fontSize=PDF_STYLE['small_font_size'],
            alignment=TA_CENTER,
            spaceAfter=6
        ))
    
    def generate_enhanced_report(self, student_data, filename=None):
        """
        Generate an enhanced Cambridge report card PDF with coefficients, GPA, and comments
        
        Args:
            student_data (dict): Enhanced student and grade data with coefficients
            filename (str): Optional custom filename
            
        Returns:
            str: Path to generated PDF file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            student_name = student_data.get('name', 'Student').replace(' ', '_')
            filename = f"{student_name}_Cambridge_Enhanced_Report_{timestamp}.pdf"
        
        # Ensure reports directory exists
        reports_dir = APP_SETTINGS['report_folder']
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)
        
        filepath = os.path.join(reports_dir, filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(
            filepath,
            pagesize=A4,
            rightMargin=PDF_STYLE['margin'],
            leftMargin=PDF_STYLE['margin'],
            topMargin=PDF_STYLE['margin'],
            bottomMargin=PDF_STYLE['margin']
        )
        
        # Build enhanced content
        story = []
        
        # Title and header
        story.extend(self._create_enhanced_header(student_data))
        
        # Student information
        story.extend(self._create_enhanced_student_info(student_data))
        
        # Enhanced grades table with coefficients
        story.extend(self._create_enhanced_grades_table(student_data))
        
        # GPA summary
        story.extend(self._create_gpa_summary(student_data))
        
        # Comments section
        if any(subject.get('comment', '') for subject in student_data.get('subjects', [])):
            story.extend(self._create_comments_section(student_data))
        
        # Footer
        story.extend(self._create_enhanced_footer())
        
        # Build PDF
        doc.build(story)
        
        return filepath
        
        # Student information
        story.extend(self._create_student_info(student_data))
        
        # Subject grades table
        story.extend(self._create_grades_table(student_data))
        
        # Final grade summary
        story.extend(self._create_final_grade_summary(student_data))
        
        # Footer
        story.extend(self._create_footer(student_data))
        
        # Build PDF
        doc.build(story)
        
        return filepath
    
    def _create_header(self, student_data):
        """Create the report header"""
        content = []
        
        # Main title
        title = Paragraph("Cambridge International Examination", self.styles['CustomTitle'])
        content.append(title)
        
        # Report type
        subtitle = Paragraph("Academic Report Card", self.styles['CustomHeader'])
        content.append(subtitle)
        
        content.append(Spacer(1, 15))  # Reduced from 20 to 15
        
        return content
    
    def _create_student_info(self, student_data):
        """Create student information section"""
        content = []
        
        # Student details table
        student_info = [
            ['Student Name:', student_data.get('name', 'N/A')],
            ['Candidate Number:', student_data.get('candidate_number', 'N/A')],
            ['Exam Session:', student_data.get('exam_session', 'N/A')],
            ['School:', student_data.get('school', APP_SETTINGS['default_school'])],
            ['Date of Report:', datetime.now().strftime("%B %d, %Y")]
        ]
        
        table = Table(student_info, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey)
        ]))
        
        content.append(table)
        content.append(Spacer(1, 12))  # Reduced from 20 to 12 for tighter spacing
        
        return content
    
    def _create_grades_table(self, student_data):
        """Create the main grades table"""
        content = []
        
        # Section header
        header = Paragraph("Subject Grades and Performance", self.styles['CustomHeader'])
        content.append(header)
        content.append(Spacer(1, 8))  # Reduced from 15 to 8
        
        # Table headers
        table_data = [
            ['Subject', 'Coeff', 'Score', 'Grade', 'Weighted Score', 'Teacher Comments']
        ]
        
        # Add subject data
        subjects = student_data.get('subjects', [])
        for subject in subjects:
            # Use Paragraph for proper HTML break handling
            subject_name = self._wrap_text(subject.get('name', 'N/A'), 24)  # Increased from 18 to 24 (added 6 chars)
            comment_text = self._wrap_text(subject.get('comment', 'No comment provided'), 30)
            
            row = [
                Paragraph(subject_name, self.styles['Normal']),  # Use Paragraph for HTML breaks
                str(subject.get('coefficient', 'N/A')),
                str(subject.get('score', 'N/A')),  # Removed % symbol
                subject.get('grade', 'N/A'),
                f"{subject.get('weighted_score', 'N/A')}",
                Paragraph(comment_text, self.styles['Normal'])   # Use Paragraph for comments too
            ]
            table_data.append(row)
        
        # Create table with adjusted column widths - moved space from Coeff to Subject
        table = Table(table_data, colWidths=[1.4*inch, 0.5*inch, 0.6*inch, 0.5*inch, 1.2*inch, 2.8*inch])
        table.setStyle(TableStyle([
            # Header row styling
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),  # Reduced from 10 to 9
            
            # Data rows styling
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),  # Reduced from 9 to 8
            ('VALIGN', (0, 1), (-1, -1), 'TOP'),
            
            # Comments column alignment
            ('ALIGN', (-1, 1), (-1, -1), 'LEFT'),
            
            # Grid and borders
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        
        content.append(table)
        content.append(Spacer(1, 20))  # Reduced from 30 to 20
        
        return content
    
    def _create_final_grade_summary(self, student_data):
        """Create final grade summary section"""
        content = []
        
        # Section header
        header = Paragraph("Final Grade Summary", self.styles['CustomHeader'])
        content.append(header)
        content.append(Spacer(1, 8))  # Reduced from 15 to 8
        
        # Summary data
        final_data = student_data.get('final_grade', {})
        summary_data = [
            ['Total Weighted Score:', f"{final_data.get('total_weighted_score', 'N/A')}"],
            ['Total Coefficient Sum:', f"{final_data.get('total_coefficient', 'N/A')}"],
            ['Weighted Average:', f"{final_data.get('weighted_average', 'N/A')}%"],
            ['Final Cambridge Grade:', final_data.get('final_grade', 'N/A')]
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.darkblue),
            ('BACKGROUND', (-1, -1), (-1, -1), colors.lightblue),  # Highlight final grade
            ('FONTNAME', (-1, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (-1, -1), (-1, -1), 14),
        ]))
        
        content.append(summary_table)
        content.append(Spacer(1, 20))
        
        # Grade explanation
        explanation = Paragraph(
            "The final grade is calculated using Cambridge International's weighted average system, "
            "where each subject score is multiplied by its coefficient and the sum is divided by "
            "the total of all coefficients.",
            self.styles['CustomSmall']
        )
        content.append(explanation)
        
        return content
    
    def _create_footer(self, student_data):
        """Create report footer"""
        content = []
        
        content.append(Spacer(1, 25))  # Reduced from 40 to 25
        
        # Signature lines
        signature_data = [
            ['_' * 30, '_' * 30],
            ['Academic Coordinator', 'School Principal'],
            ['Signature & Date', 'Signature & Date']
        ]
        
        signature_table = Table(signature_data, colWidths=[3*inch, 3*inch])
        signature_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ]))
        
        content.append(signature_table)
        content.append(Spacer(1, 20))
        
        # Footer text
        footer_text = Paragraph(
            f"Generated by {APP_SETTINGS['title']} v{APP_SETTINGS['version']} | "
            f"Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            self.styles['CustomSmall']
        )
        content.append(footer_text)
        
        return content

    def _create_enhanced_header(self, student_data):
        """Create enhanced header with Cambridge branding"""
        content = []
        
        # Main title
        title = Paragraph("Cambridge International Examination", self.styles['CustomTitle'])
        content.append(title)
        content.append(Spacer(1, 10))
        
        # Subtitle
        subtitle = Paragraph("Advanced Academic Report Card", self.styles['CustomHeader'])
        content.append(subtitle)
        content.append(Spacer(1, 20))
        
        return content

    def _create_enhanced_student_info(self, student_data):
        """Create enhanced student information section"""
        content = []
        
        # Student info header
        info_header = Paragraph("Student Information", self.styles['CustomHeader'])
        content.append(info_header)
        content.append(Spacer(1, 10))
        
        # Student details table
        student_info = [
            ['Student Name:', student_data.get('name', 'N/A'), 'Candidate Number:', student_data.get('candidate_number', 'N/A')],
            ['Center Number:', student_data.get('center_number', 'N/A'), 'Session:', student_data.get('session', 'N/A')],
            ['Year:', student_data.get('year', 'N/A'), 'Total Subjects:', str(student_data.get('total_subjects', 0))],
        ]
        
        student_table = Table(student_info, colWidths=[1.5*inch, 2*inch, 1.5*inch, 2*inch])
        student_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTNAME', (3, 0), (3, -1), 'Helvetica'),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        content.append(student_table)
        content.append(Spacer(1, 20))
        
        return content

    def _create_enhanced_grades_table(self, student_data):
        """Create enhanced grades table with coefficients and weighted scores"""
        content = []
        
        # Grades header
        grades_header = Paragraph("Academic Performance", self.styles['CustomHeader'])
        content.append(grades_header)
        content.append(Spacer(1, 10))
        
        # Table headers
        headers = ['Subject', 'Raw Score', 'Letter Grade', 'Coefficient', 'Grade Points', 'Weighted Score']
        table_data = [headers]
        
        # Add subject data
        for subject in student_data.get('subjects', []):
            row = [
                self._wrap_text(subject.get('name', ''), 25),
                f"{subject.get('score', 0):.1f}",
                subject.get('letter_grade', 'U'),
                f"{subject.get('coefficient', 1.0):.1f}",
                f"{subject.get('grade_points', 0.0):.1f}",
                f"{subject.get('weighted_score', 0.0):.1f}"
            ]
            table_data.append(row)
        
        # Create table
        grades_table = Table(table_data, colWidths=[2.2*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch, 1*inch])
        
        # Style the table
        style = [
            ('BACKGROUND', (0, 0), (-1, 0), colors.navy),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),  # Subject names left-aligned
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]
        
        # Alternate row colors
        for i in range(1, len(table_data)):
            if i % 2 == 0:
                style.append(('BACKGROUND', (0, i), (-1, i), colors.lightgrey))
        
        grades_table.setStyle(TableStyle(style))
        content.append(grades_table)
        content.append(Spacer(1, 20))
        
        return content

    def _create_gpa_summary(self, student_data):
        """Create GPA summary section"""
        content = []
        
        # GPA header
        gpa_header = Paragraph("Academic Summary", self.styles['CustomHeader'])
        content.append(gpa_header)
        content.append(Spacer(1, 10))
        
        # GPA information
        gpa = student_data.get('gpa', 0.0)
        total_subjects = student_data.get('total_subjects', 0)
        
        # Performance classification
        if gpa >= 3.5:
            classification = "Distinction"
            perf_color = colors.darkgreen
        elif gpa >= 3.0:
            classification = "Merit"
            perf_color = colors.orange
        elif gpa >= 2.5:
            classification = "Credit"
            perf_color = colors.blue
        elif gpa >= 2.0:
            classification = "Pass"
            perf_color = colors.black
        else:
            classification = "Below Standard"
            perf_color = colors.red
        
        # GPA summary table
        gpa_data = [
            ['Overall GPA:', f"{gpa:.2f}/4.0", 'Classification:', classification],
            ['Total Subjects:', str(total_subjects), 'Performance Level:', classification]
        ]
        
        gpa_table = Table(gpa_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        gpa_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
            ('TEXTCOLOR', (1, 0), (1, 0), perf_color),
            ('TEXTCOLOR', (3, 0), (3, -1), perf_color),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        
        content.append(gpa_table)
        content.append(Spacer(1, 20))
        
        return content

    def _create_comments_section(self, student_data):
        """Create teacher comments section"""
        content = []
        
        # Comments header
        comments_header = Paragraph("Teacher Comments", self.styles['CustomHeader'])
        content.append(comments_header)
        content.append(Spacer(1, 10))
        
        # Add comments for each subject
        for subject in student_data.get('subjects', []):
            comment = subject.get('comment', '').strip()
            if comment:
                subject_name = subject.get('name', 'Unknown Subject')
                comment_text = f"<b>{subject_name}:</b> {comment}"
                comment_para = Paragraph(comment_text, self.styles['CustomBody'])
                content.append(comment_para)
                content.append(Spacer(1, 8))
        
        content.append(Spacer(1, 10))
        return content

    def _create_enhanced_footer(self):
        """Create enhanced footer with additional information"""
        content = []
        
        # Signature section
        content.append(Spacer(1, 30))
        
        signature_data = [
            ['Principal Signature', 'Date'],
            ['_' * 30, '_' * 20],
        ]
        
        signature_table = Table(signature_data, colWidths=[3*inch, 3*inch])
        signature_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ]))
        
        content.append(signature_table)
        content.append(Spacer(1, 20))
        
        # Enhanced footer text
        footer_text = Paragraph(
            f"Generated by {APP_SETTINGS['title']} v{APP_SETTINGS['version']} | "
            f"Enhanced Report with Weighted Grading | "
            f"Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            self.styles['CustomSmall']
        )
        content.append(footer_text)
        
        return content
    
    def _wrap_text(self, text, max_length):
        """Wrap text to fit in table cells"""
        if len(text) <= max_length:
            return text
        
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 <= max_length:
                current_line.append(word)
                current_length += len(word) + 1
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
                current_length = len(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return '<br/>'.join(lines)
    
    def generate_sample_report(self):
        """Generate a sample report for testing"""
        sample_data = {
            'name': 'John Smith',
            'candidate_number': 'CB123456',
            'exam_session': 'June 2024',
            'school': 'Cambridge International School',
            'subjects': [
                {
                    'name': 'Mathematics',
                    'coefficient': 2.0,
                    'score': 85,
                    'grade': 'A',
                    'weighted_score': 170.0,
                    'comment': 'Excellent problem-solving skills and strong understanding of algebraic concepts.'
                },
                {
                    'name': 'Physics',
                    'coefficient': 1.8,
                    'score': 78,
                    'grade': 'B',
                    'weighted_score': 140.4,
                    'comment': 'Good grasp of fundamental principles. Needs improvement in practical applications.'
                },
                {
                    'name': 'English Literature',
                    'coefficient': 1.5,
                    'score': 92,
                    'grade': 'A*',
                    'weighted_score': 138.0,
                    'comment': 'Outstanding analytical skills and excellent written expression.'
                }
            ],
            'final_grade': {
                'total_weighted_score': 448.4,
                'total_coefficient': 5.3,
                'weighted_average': 84.6,
                'final_grade': 'A'
            }
        }
        
        return self.generate_report(sample_data, 'sample_cambridge_report.pdf')