@echo off
REM Quick installation script for Windows

echo 🚀 Installing Cambridge Exam System...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is required. Please install Python 3.8+ first.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo 📥 Installing dependencies...
pip install -r requirements.txt

echo ✅ Installation complete!
echo 🎯 Run the application with: run.bat
echo 📝 Or manually activate venv and run: python main_gui_complete.py
pause