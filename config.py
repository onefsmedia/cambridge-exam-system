"""
Cambridge Exam Report Card System Configuration
Contains subjects, coefficients, and grade thresholds following Cambridge International standards
"""

# Cambridge subjects with their official coefficients and codes
CAMBRIDGE_SUBJECTS = {
    # Mathematics
    '0580': {'name': 'Mathematics', 'coefficient': 1.2},
    '0606': {'name': 'Additional Mathematics', 'coefficient': 1.3},
    '9709': {'name': 'Mathematics (A Level)', 'coefficient': 1.5},
    
    # Sciences
    '0620': {'name': 'Chemistry', 'coefficient': 1.2},
    '0625': {'name': 'Physics', 'coefficient': 1.2},
    '0610': {'name': 'Biology', 'coefficient': 1.2},
    '0654': {'name': 'Co-ordinated Sciences (Double Award)', 'coefficient': 1.1},
    '0653': {'name': 'Combined Science', 'coefficient': 1.1},
    '9701': {'name': 'Chemistry (A Level)', 'coefficient': 1.5},
    '9702': {'name': 'Physics (A Level)', 'coefficient': 1.5},
    '9700': {'name': 'Biology (A Level)', 'coefficient': 1.5},
    
    # Languages - English
    '0500': {'name': 'First Language English', 'coefficient': 1.3},
    '0510': {'name': 'English as a Second Language', 'coefficient': 1.2},
    '0522': {'name': 'First Language English (US)', 'coefficient': 1.3},
    '9093': {'name': 'English Language (A Level)', 'coefficient': 1.4},
    '9695': {'name': 'Literature in English (A Level)', 'coefficient': 1.4},
    
    # Languages - Other
    '0520': {'name': 'French', 'coefficient': 1.1},
    '0530': {'name': 'Spanish', 'coefficient': 1.1},
    '0525': {'name': 'German', 'coefficient': 1.1},
    '0515': {'name': 'Arabic', 'coefficient': 1.1},
    '0547': {'name': 'Mandarin Chinese', 'coefficient': 1.1},
    '0518': {'name': 'Hindi', 'coefficient': 1.1},
    
    # Humanities
    '0470': {'name': 'History', 'coefficient': 1.2},
    '0460': {'name': 'Geography', 'coefficient': 1.2},
    '0495': {'name': 'Sociology', 'coefficient': 1.1},
    '9489': {'name': 'History (A Level)', 'coefficient': 1.4},
    '9696': {'name': 'Geography (A Level)', 'coefficient': 1.4},
    
    # Business and Economics
    '0450': {'name': 'Business Studies', 'coefficient': 1.2},
    '0455': {'name': 'Economics', 'coefficient': 1.2},
    '0452': {'name': 'Accounting', 'coefficient': 1.2},
    '9707': {'name': 'Business Studies (A Level)', 'coefficient': 1.4},
    '9708': {'name': 'Economics (A Level)', 'coefficient': 1.4},
    
    # Computer Science and ICT
    '0478': {'name': 'Computer Science', 'coefficient': 1.3},
    '0417': {'name': 'Information and Communication Technology', 'coefficient': 1.2},
    '9618': {'name': 'Computer Science (A Level)', 'coefficient': 1.5},
    '9626': {'name': 'Information Technology (A Level)', 'coefficient': 1.4},
    
    # Arts and Design
    '0400': {'name': 'Art & Design', 'coefficient': 1.0},
    '0410': {'name': 'Music', 'coefficient': 1.0},
    '0419': {'name': 'Food and Nutrition', 'coefficient': 1.0},
    '0445': {'name': 'Design and Technology', 'coefficient': 1.1},
    '9479': {'name': 'Art & Design (A Level)', 'coefficient': 1.2},
    
    # Physical Education and Sports
    '0413': {'name': 'Physical Education', 'coefficient': 1.0},
    '9396': {'name': 'Physical Education (A Level)', 'coefficient': 1.2},
    
    # Additional Subjects
    '0490': {'name': 'Religious Studies', 'coefficient': 1.0},
    '0509': {'name': 'First Language Chinese', 'coefficient': 1.2},
    '0544': {'name': 'Arabic (Foreign Language)', 'coefficient': 1.1},
    '0549': {'name': 'Hindi as a Second Language', 'coefficient': 1.1},
    
    # Environmental and Global Studies
    '0680': {'name': 'Environmental Management', 'coefficient': 1.1},
    '0457': {'name': 'Global Perspectives', 'coefficient': 1.0},
    
    # Psychology and Philosophy
    '9990': {'name': 'Psychology (A Level)', 'coefficient': 1.4},
    '9774': {'name': 'Philosophy (A Level)', 'coefficient': 1.3},
    
    # Media and Communication
    '0607': {'name': 'Media Studies', 'coefficient': 1.0},
    '9607': {'name': 'Media Studies (A Level)', 'coefficient': 1.3},
}

# Official Cambridge IGCSE/AS&A-Level grade thresholds - range A* to U
GRADE_THRESHOLDS = [
    {"min": 90, "max": 100, "grade": "A*"},
    {"min": 80, "max": 89, "grade": "A"},
    {"min": 70, "max": 79, "grade": "B"},
    {"min": 60, "max": 69, "grade": "C"},
    {"min": 50, "max": 59, "grade": "D"},
    {"min": 40, "max": 49, "grade": "E"},
    {"min": 30, "max": 39, "grade": "F"},
    {"min": 20, "max": 29, "grade": "G"},
    {"min": 0, "max": 19, "grade": "U"}  # Ungraded for scores below 20
]

# Application settings
APP_SETTINGS = {
    "title": "Cambridge Exam Report Card Generator",
    "version": "1.0.0",
    "max_subjects": 8,
    "min_score": 0,
    "max_score": 100,
    "default_school": "Cambridge International School",
    "report_folder": "reports",
    "examination_sessions": [
        "May/June 2024",
        "October/November 2024",
        "February/March 2025",
        "May/June 2025",
        "October/November 2025"
    ]
}

# PDF styling settings
PDF_STYLE = {
    "page_size": "A4",
    "margin": 30,
    "title_font_size": 16,  # Reduced from 20 to 16
    "header_font_size": 14,  # Reduced from 16 to 14
    "body_font_size": 10,  # Reduced from 12 to 10
    "small_font_size": 9,  # Reduced from 10 to 9
    "line_height": 12  # Reduced from 14 to 12
}

def get_subject_coefficient(subject_name):
    """Get coefficient for a specific subject"""
    for subject in CAMBRIDGE_SUBJECTS:
        if subject["name"] == subject_name:
            return subject["coefficient"]
    return 1.0  # Default coefficient if subject not found

def get_subject_names():
    """Get list of all subject names"""
    return [subject["name"] for subject in CAMBRIDGE_SUBJECTS]

def generate_candidate_number():
    """Generate a unique candidate number"""
    import random
    from datetime import datetime
    
    # Format: CB + Year(2 digits) + Random 4 digits
    year = datetime.now().year % 100  # Last 2 digits of year
    random_part = random.randint(1000, 9999)
    return f"CB{year:02d}{random_part}"

def update_subject_coefficient(subject_name, new_coefficient):
    """Update coefficient for a specific subject"""
    for subject in CAMBRIDGE_SUBJECTS:
        if subject["name"] == subject_name:
            subject["coefficient"] = float(new_coefficient)
            return True
    return False

def reset_coefficients_to_default():
    """Reset all coefficients to their default values"""
    default_subjects = [
        {"name": "Mathematics", "coefficient": 2.0},
        {"name": "Physics", "coefficient": 1.8},
        {"name": "English Literature", "coefficient": 1.5},
        {"name": "Biology", "coefficient": 1.7},
        {"name": "History", "coefficient": 1.3},
        {"name": "Chemistry", "coefficient": 1.8},
        {"name": "Geography", "coefficient": 1.4},
        {"name": "Economics", "coefficient": 1.6},
        {"name": "Computer Science", "coefficient": 1.9},
        {"name": "Art & Design", "coefficient": 1.2}
    ]
    
    global CAMBRIDGE_SUBJECTS
    CAMBRIDGE_SUBJECTS.clear()
    CAMBRIDGE_SUBJECTS.extend(default_subjects)