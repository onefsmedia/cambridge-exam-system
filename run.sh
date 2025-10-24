#!/bin/bash
# Run script for Unix/Linux/macOS

echo "🎯 Starting Cambridge Exam System..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run install.sh first."
    exit 1
fi

# Activate virtual environment and run
source venv/bin/activate
python main_gui_complete.py