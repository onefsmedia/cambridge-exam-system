#!/bin/bash
# Quick installation script for Unix/Linux/macOS

echo "🚀 Installing Cambridge Exam System..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required. Please install Python 3.8+ first."
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Make script executable
chmod +x run.sh

echo "✅ Installation complete!"
echo "🎯 Run the application with: ./run.sh"
echo "📝 Or manually with: source venv/bin/activate && python main_gui_complete.py"