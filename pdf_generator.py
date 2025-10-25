"""
PDF Report Generator for Cambridge Exam Report Cards
Uses reportlab to create professional-looking PDF reports
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from datetime import datetime
import os
from config import PDF_STYLE, APP_SETTINGS

class CambridgePDFGenerator:
    """Generate Cambridge-style report card PDFs"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom paragraph styles matching Joe's template"""
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
        
        # Legacy styles for backward compatibility
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=PDF_STYLE['title_font_size'],
            alignment=TA_CENTER,
            spaceAfter=30,
            textColor=colors.darkblue
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeader',
            parent=self.styles['Heading2'],
            fontSize=PDF_STYLE['header_font_size'],
            alignment=TA_CENTER,
            spaceAfter=20
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=PDF_STYLE['body_font_size'],
            alignment=TA_LEFT,
            spaceAfter=12
        ))
        
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
        
        # Enhanced grades table with coefficients and teacher comments
        story.extend(self._create_enhanced_grades_table(student_data))
        
        # GPA summary
        story.extend(self._create_gpa_summary(student_data))
        
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
        """Create Cambridge International Examinations header matching Joe's template"""
        content = []
        
        # School name (centered) - use dynamic school name if provided
        school_name_text = student_data.get('school_name', 'DOBEDA INTERNATIONAL SCHOOL')
        school_name = Paragraph(school_name_text.upper(), self.styles['CambridgeTitle'])
        content.append(school_name)
        
        # Main Cambridge title (centered)
        cambridge_title = Paragraph("CAMBRIDGE INTERNATIONAL EXAMINATIONS", self.styles['CambridgeSubtitle'])
        content.append(cambridge_title)
        
        # Statement of Results (centered)
        statement = Paragraph("STATEMENT OF RESULTS", self.styles['CambridgeDocType'])
        content.append(statement)
        
        content.append(Spacer(1, 15))
        
        return content

    def _create_enhanced_student_info(self, student_data):
        """Create student information section matching Joe's template"""
        content = []
        
        # Student info table data matching Joe's template with dynamic values
        info_data = [
            ['Centre Number:', student_data.get('centre_number', '12345'), 'Session:', student_data.get('session', 'June 2024')],
            ['Candidate Name:', student_data.get('student_name', student_data.get('name', 'Unknown')), 'Candidate Number:', '  ' + student_data.get('candidate_number', '0001')],
        ]
        
        # Create table with proper spacing - adjusted to prevent text overlap
        info_table = Table(info_data, colWidths=[1.3*inch, 1.7*inch, 1.5*inch, 1.1*inch])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 3),
            ('RIGHTPADDING', (2, 1), (2, 1), 8),  # Extra padding for "Candidate Number:" label
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            # Bold the labels only
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ]))
        
        content.append(info_table)
        content.append(Spacer(1, 20))
        
        return content

    def _create_enhanced_grades_table(self, student_data):
        """Create enhanced grades table - Joe's template style"""
        content = []
        
        # Main results header - centered
        results_header = Paragraph(
            "<b>Subject Results</b>",
            ParagraphStyle(
                name='ResultsHeader',
                fontSize=12,
                alignment=TA_CENTER,
                spaceAfter=10,
                textColor=colors.black,
                fontName='Helvetica-Bold'
            )
        )
        content.append(results_header)
        
        # Table headers with Cambridge style - abbreviated and properly spaced
        headers = ['Subject', 'Coeff', 'Score', 'Grade', 'W. Score', 'Teacher Comments']
        table_data = [headers]
        
        # Add subject data
        for subject in student_data.get('subjects', []):
            subject_name = subject.get('name', '')
            
            # Get teacher comments - look for multiple possible field names
            teacher_comment = (
                subject.get('teacher_comments', '') or 
                subject.get('comment', '') or 
                subject.get('comments', '') or 
                'Good'  # Default comment
            )
            
            row = [
                self._wrap_text(subject_name, 30),
                f"{subject.get('coefficient', 1.0):.1f}",
                f"{subject.get('score', 0):.0f}%",
                subject.get('grade', subject.get('letter_grade', 'U')),
                f"{subject.get('weighted_score', subject.get('score', 0) * subject.get('coefficient', 1.0)):.1f}",
                self._wrap_text(teacher_comment, 25)
            ]
            table_data.append(row)
        
        # Create table with Cambridge-style formatting - wider columns for Subject and Teacher Comments
        grades_table = Table(table_data, colWidths=[2.2*inch, 0.7*inch, 0.7*inch, 0.6*inch, 0.8*inch, 1.6*inch])
        
        # Style the table with clean Cambridge formatting and proper alignment
        style = [
            # Header row styling
            ('BACKGROUND', (0, 0), (-1, 0), colors.white),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),    # Subject column header left-aligned
            ('ALIGN', (1, 0), (1, 0), 'CENTER'),  # Coeff header center
            ('ALIGN', (2, 0), (2, 0), 'CENTER'),  # Score header center
            ('ALIGN', (3, 0), (3, 0), 'CENTER'),  # Grade header center
            ('ALIGN', (4, 0), (4, 0), 'CENTER'),  # W. Score header center
            ('ALIGN', (5, 0), (5, 0), 'LEFT'),    # Teacher Comments header left
            
            # Data rows styling
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),    # Subject names left-aligned
            ('ALIGN', (1, 1), (1, -1), 'CENTER'),  # Coefficient values center
            ('ALIGN', (2, 1), (2, -1), 'CENTER'),  # Score values center
            ('ALIGN', (3, 1), (3, -1), 'CENTER'),  # Grade values center
            ('ALIGN', (4, 1), (4, -1), 'CENTER'),  # W. Score values center
            ('ALIGN', (5, 1), (5, -1), 'LEFT'),    # Teacher Comments left-aligned
            
            # Borders - clean professional lines with top border
            ('LINEABOVE', (0, 0), (-1, 0), 2, colors.black),  # Bold line ABOVE header (top border)
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),  # Bold line under header
            ('LINEBELOW', (0, 1), (-1, -1), 0.5, colors.gray),  # Light lines under data rows
            ('LINEBEFORE', (0, 0), (0, -1), 1, colors.black),  # Left border
            ('LINEAFTER', (-1, 0), (-1, -1), 1, colors.black),  # Right border
            ('LINEAFTER', (0, 0), (0, -1), 0.5, colors.gray),  # Subject column separator
            ('LINEAFTER', (1, 0), (1, -1), 0.5, colors.gray),  # Coeff column separator
            ('LINEAFTER', (2, 0), (2, -1), 0.5, colors.gray),  # Score column separator
            ('LINEAFTER', (3, 0), (3, -1), 0.5, colors.gray),  # Grade column separator
            ('LINEAFTER', (4, 0), (4, -1), 0.5, colors.gray),  # W. Score column separator
            ('LINEAFTER', (3, 0), (3, -1), 0.5, colors.gray),  # Grade column separator
            ('LINEAFTER', (4, 0), (4, -1), 0.5, colors.gray),  # Weighted Score column separator
            
            # Padding for better readability
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]
        
        grades_table.setStyle(TableStyle(style))
        content.append(grades_table)
        content.append(Spacer(1, 25))
        
        return content

    def _create_gpa_summary(self, student_data):
        """Create GPA summary section with Cambridge styling"""
        content = []
        
        # Summary header with Cambridge style
        summary_header = Paragraph("PERFORMANCE SUMMARY", 
                                 getSampleStyleSheet()['Heading1'])
        summary_header.style.alignment = 1  # Center
        summary_header.style.fontSize = 14
        summary_header.style.fontName = 'Helvetica-Bold'
        summary_header.style.spaceAfter = 12
        content.append(summary_header)
        
        # Calculate GPA and classification
        gpa = student_data.get('gpa', 0.0)
        total_subjects = student_data.get('total_subjects', 0)
        
        # Cambridge A-Level Performance Classification
        if gpa >= 3.7:
            classification = "DISTINCTION"
            grade_range = "A* - A"
        elif gpa >= 3.0:
            classification = "MERIT"
            grade_range = "A - B"
        elif gpa >= 2.3:
            classification = "CREDIT"
            grade_range = "B - C"
        elif gpa >= 2.0:
            classification = "PASS"
            grade_range = "C - D"
        else:
            classification = "UNCLASSIFIED"
            grade_range = "Below D"
        
        # Summary table with Cambridge formatting
        summary_data = [
            ['Overall Grade Point Average:', f"{gpa:.2f}"],
            ['Total Subjects Attempted:', str(total_subjects)],
            ['Performance Classification:', classification],
            ['Grade Range:', grade_range]
        ]
        
        summary_table = Table(summary_data, colWidths=[3.5*inch, 2.5*inch])
        summary_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            # Bold the classification row
            ('FONTNAME', (0, 2), (-1, 2), 'Helvetica-Bold'),
        ]))
        
        content.append(summary_table)
        content.append(Spacer(1, 20))
        
        return content

    def _create_comments_section(self, student_data):
        """Create teacher comments section matching Joe's template"""
        content = []
        
        # Comments header
        comments_header = Paragraph("Teacher Comments:", self.styles['JoeBodyTextBold'])
        content.append(comments_header)
        content.append(Spacer(1, 10))
        
        # Add comments for each subject
        for subject in student_data.get('subjects', []):
            comment = subject.get('teacher_comments', subject.get('comment', '')).strip()
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

    def _create_enhanced_footer(self):
        """Create footer with DOBEDA copyright matching Joe's template"""
        content = []
        
        # Add significant space before footer
        content.append(Spacer(1, 40))
        
        # Signature lines
        sig_data = [
            ['_' * 30, '_' * 30],
            ['Academic Coordinator', 'School Principal'],
            ['Signature & Date', 'Signature & Date']
        ]
        
        sig_table = Table(sig_data, colWidths=[3*inch, 3*inch])
        sig_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ]))
        
        content.append(sig_table)
        content.append(Spacer(1, 30))
        
        # DOBEDA copyright footer
        footer_text = Paragraph("© 2025 DOBEDA - Cambridge Examination Report System", self.styles['JoeFooter'])
        content.append(footer_text)
        
        return content
    
    def _wrap_text(self, text, max_length):
        """Wrap text to fit in table cells, breaking only between words"""
        if len(text) <= max_length:
            return text
        
        # Remove any existing HTML tags
        text = text.replace('<br/>', ' ').replace('<br>', ' ')
        
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            # Calculate the length of current line if this word is added
            test_length = current_length + len(word) + (1 if current_line else 0)  # +1 for space
            
            if test_length <= max_length:
                current_line.append(word)
                current_length = test_length
            else:
                # If current line has words, save it and start new line
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                    current_length = len(word)
                else:
                    # Single word too long, just add it
                    lines.append(word)
                    current_line = []
                    current_length = 0
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Return joined lines with newline characters for ReportLab
        return '\n'.join(lines)
    
    def generate_sample_report(self):
        """Generate a sample report for testing"""
        sample_data = {
            'name': 'Sample Student',
            'candidate_number': '0001',
            'exam_session': 'October 2025',
            'school': 'Sample School',
            'subjects': [
                {
                    'name': 'Mathematics',
                    'coefficient': 2.0,
                    'score': 90,
                    'grade': 'A*',
                    'weighted_score': 180.0,
                    'comment': 'Excellent performance with strong analytical skills.'
                },
                {
                    'name': 'English Language',
                    'coefficient': 1.5,
                    'score': 85,
                    'grade': 'A',
                    'weighted_score': 127.5,
                    'comment': 'Very good communication and writing abilities.'
                },
                {
                    'name': 'Science',
                    'coefficient': 1.8,
                    'score': 88,
                    'grade': 'A',
                    'weighted_score': 158.4,
                    'comment': 'Strong understanding of scientific concepts.'
                }
            ],
            'final_grade': {
                'total_weighted_score': 465.9,
                'total_coefficient': 5.3,
                'weighted_average': 87.9,
                'final_grade': 'A*'
            }
        }
        
        return self.generate_report(sample_data, 'sample_cambridge_report.pdf')