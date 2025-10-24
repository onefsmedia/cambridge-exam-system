@echo off
REM Run script for Windows

echo 🎯 Starting Cambridge Exam System...

REM Check if virtual environment exists
if not exist "venv" (
    echo ❌ Virtual environment not found. Please run install.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment and run
call venv\Scripts\activate.bat
python main_gui_complete.py