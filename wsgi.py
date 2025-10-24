"""
WSGI configuration for CloudPanel deployment
"""

import sys
import os

# Add the application directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from app import app

# WSGI callable
application = app

if __name__ == "__main__":
    app.run()