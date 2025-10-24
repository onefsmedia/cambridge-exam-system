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
from pdf_generator import CambridgePDFGenerator
from config import CAMBRIDGE_SUBJECTS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'cambridge_exam_system_2024_secure_key'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create necessary directories
UPLOAD_FOLDER = 'uploads'
REPORTS_FOLDER = 'reports'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORTS_FOLDER, exist_ok=True)

@app.route('/')
def index():
    """Main page with the report form"""
    return render_template('index.html', subjects=CAMBRIDGE_SUBJECTS)

@app.route('/api/subjects')
def get_subjects():
    """API endpoint to get all subjects"""
    return jsonify(CAMBRIDGE_SUBJECTS)

@app.route('/generate_report', methods=['POST'])
def generate_report():
    """Generate PDF report from form data"""
    try:
        # Get form data
        student_data = {
            'name': request.form.get('student_name', ''),
            'candidate_number': request.form.get('candidate_number', ''),
            'center_number': request.form.get('center_number', ''),
            'session': request.form.get('session', ''),
            'year': request.form.get('year', ''),
            'subjects': []
        }
        
        # Parse subject data
        subject_count = int(request.form.get('subject_count', 0))
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
                except ValueError:
                    flash(f'Invalid score for {subject_name}', 'error')
                    return redirect(url_for('index'))
        
        if not student_data['subjects']:
            flash('Please add at least one subject with a valid score', 'error')
            return redirect(url_for('index'))
        
        # Generate PDF
        pdf_generator = CambridgePDFGenerator()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cambridge_report_{timestamp}.pdf"
        filepath = os.path.join(REPORTS_FOLDER, filename)
        
        # Generate the PDF
        pdf_generator.generate_report(student_data, filepath)
        
        logger.info(f"Generated report: {filename}")
        return send_file(filepath, as_attachment=True, download_name=filename)
        
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        flash(f'Error generating report: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/preview')
def preview():
    """Preview page to show how the report will look"""
    return render_template('preview.html', subjects=CAMBRIDGE_SUBJECTS)

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # For development
    app.run(host='0.0.0.0', port=5000, debug=True)