#!/usr/bin/env python3
"""
Cambridge Exam System - Web Version
Flask web application for CloudPanel VPS deployment
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

@app.route('/')
def index():
    """Main page with the report form"""
    logger.info("Index page accessed")
    return render_template('index.html', subjects=CAMBRIDGE_SUBJECTS)

@app.route('/api/subjects')
def get_subjects():
    """API endpoint to get all subjects"""
    logger.info("Subjects API accessed")
    return jsonify(CAMBRIDGE_SUBJECTS)

@app.route('/generate_report', methods=['POST'])
def generate_report():
    """Generate PDF report from form data"""
    try:
        logger.info("Report generation requested")
        
        # Get form data
        student_data = {
            'name': request.form.get('student_name', ''),
            'candidate_number': request.form.get('candidate_number', ''),
            'center_number': request.form.get('center_number', ''),
            'session': request.form.get('session', ''),
            'year': request.form.get('year', ''),
            'subjects': []
        }
        
        logger.info(f"Processing report for student: {student_data['name']}")
        
        # Parse subject data
        subject_count = int(request.form.get('subject_count', 0))
        logger.info(f"Processing {subject_count} subjects")
        
        for i in range(subject_count):
            subject_name = request.form.get(f'subject_{i}')
            raw_score = request.form.get(f'score_{i}')
            
            if subject_name and raw_score:
                try:
                    score = float(raw_score)
                    if 0 <= score <= 100:
                        student_data['subjects'].append({
                            'name': subject_name,
                            'score': score
                        })
                        logger.info(f"Added subject: {subject_name} with score: {score}")
                except ValueError:
                    error_msg = f'Invalid score for {subject_name}'
                    logger.error(error_msg)
                    flash(error_msg, 'error')
                    return redirect(url_for('index'))
        
        if not student_data['subjects']:
            error_msg = 'Please add at least one subject with a valid score'
            logger.error(error_msg)
            flash(error_msg, 'error')
            return redirect(url_for('index'))
        
        # Generate PDF
        logger.info("Generating PDF report")
        pdf_generator = CambridgePDFGenerator()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cambridge_report_{timestamp}.pdf"
        filepath = os.path.join(REPORTS_FOLDER, filename)
        
        # Generate the PDF
        pdf_generator.generate_report(student_data, filepath)
        
        logger.info(f"Generated report: {filename}")
        return send_file(filepath, as_attachment=True, download_name=filename)
        
    except Exception as e:
        error_msg = f"Error generating report: {str(e)}"
        logger.error(error_msg, exc_info=True)
        flash(error_msg, 'error')
        return redirect(url_for('index'))

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