#!/usr/bin/env python3
"""
Cambridge Exam System - Web Version (Enhanced)
Flask web application for CloudPanel VPS deployment
Matches desktop GUI functionality with advanced features
"""

from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
import json
import tempfile
from datetime import datetime
import logging
import sys
from pdf_generator import CambridgePDFGenerator
from config import CAMBRIDGE_SUBJECTS
from cambridge_calculator import CambridgeCalculator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'cambridge_exam_system_2024_secure_key')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create necessary directories
UPLOAD_FOLDER = 'uploads'
REPORTS_FOLDER = 'reports'
LOGS_FOLDER = 'logs'

for folder in [UPLOAD_FOLDER, REPORTS_FOLDER, LOGS_FOLDER]:
    os.makedirs(folder, exist_ok=True)
    logger.info(f"Created/verified directory: {folder}")

# Initialize calculator
try:
    calculator = CambridgeCalculator()
    logger.info("Cambridge calculator initialized successfully")
except Exception as e:
    calculator = None
    logger.error(f"Failed to initialize calculator: {e}")

@app.route('/')
def index():
    """Main page with enhanced report form matching desktop GUI"""
    logger.info("Index page accessed")
    return render_template('index.html', subjects=CAMBRIDGE_SUBJECTS)

@app.route('/legacy')
def legacy_index():
    """Legacy simple form for backwards compatibility"""
    logger.info("Legacy index page accessed")
    return render_template('index.html', subjects=CAMBRIDGE_SUBJECTS)

@app.route('/api/subjects')
def get_subjects():
    """API endpoint to get all subjects"""
    logger.info("Subjects API accessed")
    return jsonify(CAMBRIDGE_SUBJECTS)

@app.route('/generate_report', methods=['POST'])
def generate_report():
    """Generate PDF report from enhanced form data with coefficients and comments"""
    try:
        logger.info("Enhanced report generation requested")
        
        # Get form data
        student_data = {
            'name': request.form.get('student_name', ''),
            'candidate_number': request.form.get('candidate_number', ''),
            'school_name': request.form.get('center_number', ''),  # Correctly map school name field
            'session': request.form.get('session', ''),
            'year': request.form.get('year', ''),
            'subjects': []
        }
        
        logger.info(f"Processing enhanced report for student: {student_data['name']}")
        
        # Parse subject data with coefficients
        subject_count = int(request.form.get('subject_count', 0))
        logger.info(f"Processing {subject_count} subjects with advanced features")
        
        total_weighted_score = 0
        total_coefficients = 0
        
        for i in range(subject_count):
            subject_name = request.form.get(f'subject_{i}')
            raw_score = request.form.get(f'score_{i}')
            coefficient = request.form.get(f'coefficient_{i}', '1.0')
            comment = request.form.get(f'comment_{i}', '')
            
            if subject_name and raw_score:
                try:
                    score = float(raw_score)
                    coeff = float(coefficient)
                    
                    if 0 <= score <= 100 and 0.1 <= coeff <= 3.0:
                        # Calculate letter grade
                        letter_grade = calculate_letter_grade(score)
                        
                        # Calculate weighted score for GPA
                        grade_points = get_grade_points(score)
                        weighted_score = grade_points * coeff
                        
                        total_weighted_score += weighted_score
                        total_coefficients += coeff
                        
                        subject_info = {
                            'name': subject_name,
                            'score': score,
                            'coefficient': coeff,
                            'letter_grade': letter_grade,
                            'grade_points': grade_points,
                            'weighted_score': weighted_score,
                            'comment': comment
                        }
                        
                        student_data['subjects'].append(subject_info)
                        logger.info(f"Added subject: {subject_name} - Score: {score}, Grade: {letter_grade}, Coeff: {coeff}")
                        
                except ValueError as e:
                    error_msg = f'Invalid data for {subject_name}: {str(e)}'
                    logger.error(error_msg)
                    flash(error_msg, 'error')
                    return redirect(url_for('index'))
        
        if not student_data['subjects']:
            error_msg = 'Please add at least one subject with valid score and coefficient'
            logger.error(error_msg)
            flash(error_msg, 'error')
            return redirect(url_for('index'))
        
        # Calculate overall GPA
        if total_coefficients > 0:
            overall_gpa = total_weighted_score / total_coefficients
            student_data['gpa'] = round(overall_gpa, 2)
            student_data['total_subjects'] = len(student_data['subjects'])
            logger.info(f"Calculated GPA: {student_data['gpa']} from {student_data['total_subjects']} subjects")
        
        # Generate enhanced PDF with all features
        try:
            pdf_generator = CambridgePDFGenerator()
            
            # Create temporary file for PDF
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf', dir=REPORTS_FOLDER) as tmp_file:
                temp_path = tmp_file.name
            
            # Generate enhanced PDF
            pdf_generator.generate_enhanced_report(student_data, temp_path)
            logger.info(f"Enhanced PDF generated successfully: {temp_path}")
            
            # Determine filename
            safe_name = secure_filename(student_data['name'].replace(' ', '_'))
            filename = f"Cambridge_Report_{safe_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            
            logger.info(f"Sending enhanced PDF: {filename}")
            return send_file(
                temp_path,
                as_attachment=True,
                download_name=filename,
                mimetype='application/pdf'
            )
            
        except Exception as e:
            error_msg = f'Error generating enhanced PDF: {str(e)}'
            logger.error(error_msg)
            flash(error_msg, 'error')
            return redirect(url_for('index'))
            
    except Exception as e:
        error_msg = f'Error processing enhanced report: {str(e)}'
        logger.error(error_msg)
        flash(error_msg, 'error')
        return redirect(url_for('index'))

def calculate_letter_grade(score):
    """Calculate letter grade from numerical score - range A* to U"""
    if score >= 90:
        return 'A*'
    elif score >= 80:
        return 'A'
    elif score >= 70:
        return 'B'
    elif score >= 60:
        return 'C'
    elif score >= 50:
        return 'D'
    elif score >= 40:
        return 'E'
    elif score >= 30:
        return 'F'
    elif score >= 20:
        return 'G'
    else:
        return 'U'  # Ungraded for scores below 20

def get_grade_points(score):
    """Convert score to grade points for GPA calculation"""
    if score >= 90:
        return 4.0
    elif score >= 80:
        return 3.7
    elif score >= 70:
        return 3.0
    elif score >= 60:
        return 2.3
    elif score >= 50:
        return 2.0
    elif score >= 40:
        return 1.7
    elif score >= 30:
        return 1.3
    elif score >= 20:
        return 1.0
    else:
        return 0.0

@app.route('/send_email', methods=['POST'])
def send_email():
    """Send report via email"""
    try:
        logger.info("Email sending requested")
        
        # Get recipient email
        recipient_email = request.form.get('recipient_email', '')
        if not recipient_email:
            return jsonify({'success': False, 'error': 'No recipient email provided'})
        
        # Get form data (same as generate_report)
        student_data = {
            'name': request.form.get('student_name', ''),
            'candidate_number': request.form.get('candidate_number', ''),
            'school': request.form.get('center_number', ''),
            'session': request.form.get('session', ''),
            'year': request.form.get('year', ''),
            'subjects': []
        }
        
        # Parse subject data with comments
        subject_count = int(request.form.get('subject_count', 0))
        total_weighted_score = 0
        total_coefficients = 0
        
        for i in range(subject_count):
            subject_name = request.form.get(f'subject_{i}')
            raw_score = request.form.get(f'score_{i}')
            coefficient = request.form.get(f'coefficient_{i}', '1.0')
            comment = request.form.get(f'comment_{i}', '')
            
            if subject_name and raw_score:
                try:
                    score = float(raw_score)
                    coeff = float(coefficient)
                    
                    if 0 <= score <= 100 and 0.1 <= coeff <= 3.0:
                        letter_grade = calculate_letter_grade(score)
                        grade_points = get_grade_points(score)
                        weighted_score = grade_points * coeff
                        
                        total_weighted_score += weighted_score
                        total_coefficients += coeff
                        
                        subject_info = {
                            'name': subject_name,
                            'score': score,
                            'coefficient': coeff,
                            'letter_grade': letter_grade,
                            'grade_points': grade_points,
                            'weighted_score': weighted_score,
                            'comment': comment
                        }
                        
                        student_data['subjects'].append(subject_info)
                        
                except ValueError:
                    continue
        
        if not student_data['subjects']:
            return jsonify({'success': False, 'error': 'No valid subjects with scores provided'})
        
        # Calculate GPA
        if total_coefficients > 0:
            overall_gpa = total_weighted_score / total_coefficients
            student_data['gpa'] = round(overall_gpa, 2)
            student_data['total_subjects'] = len(student_data['subjects'])
        
        # Generate PDF first
        try:
            pdf_generator = CambridgePDFGenerator()
            
            # Create temporary file for PDF
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf', dir=REPORTS_FOLDER) as tmp_file:
                temp_path = tmp_file.name
            
            # Generate enhanced PDF
            pdf_generator.generate_enhanced_report(student_data, temp_path)
            
            # Create email content
            subject = f"Cambridge International Examination Report - {student_data['name']}"
            
            # Simple email body (since we don't have SMTP configured, we'll return success for now)
            body = f"""
Dear Recipient,

Please find attached the Cambridge International Examination Report for:

Student: {student_data['name']}
Candidate Number: {student_data['candidate_number']}
School: {student_data['school']}
Session: {student_data['session']} {student_data['year']}
Overall GPA: {student_data.get('gpa', 'N/A')}/4.0

Total Subjects: {student_data.get('total_subjects', 0)}

Best regards,
Cambridge Exam System
"""
            
            # In a real implementation, you would send the email here
            # For now, we'll just log the action and return success
            logger.info(f"Email would be sent to {recipient_email}")
            logger.info(f"Subject: {subject}")
            logger.info(f"PDF path: {temp_path}")
            
            # Clean up temp file
            os.unlink(temp_path)
            
            return jsonify({
                'success': True, 
                'message': f'Report email prepared for {recipient_email}. Note: Email sending requires SMTP configuration.'
            })
            
        except Exception as e:
            logger.error(f"Error generating PDF for email: {str(e)}")
            return jsonify({'success': False, 'error': f'Failed to generate PDF: {str(e)}'})
            
    except Exception as e:
        logger.error(f"Error processing email request: {str(e)}")
        return jsonify({'success': False, 'error': f'Failed to process email request: {str(e)}'})

@app.route('/preview')
def preview():
    """Preview page to show how the report will look"""
    logger.info("Preview page accessed")
    return render_template('preview.html', subjects=CAMBRIDGE_SUBJECTS)

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    logger.info("Health check accessed")
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'subjects_count': len(CAMBRIDGE_SUBJECTS)
    })

@app.errorhandler(404)
def not_found(error):
    logger.warning(f"404 error: {request.url}")
    return jsonify({'error': 'Page not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"500 error: {str(error)}", exc_info=True)
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Get port from environment or default to 5000
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    logger.info(f"Starting Cambridge Exam System on {host}:{port}")
    logger.info(f"Debug mode: {debug}")
    logger.info(f"Working directory: {os.getcwd()}")
    
    # For development and production
    app.run(host=host, port=port, debug=debug)