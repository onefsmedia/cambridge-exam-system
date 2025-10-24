@echo off
echo Starting Cambridge Report Card Generator...
echo.

REM Change to the correct directory
cd /d "D:\DOBEDA\cambridge_exams\cambridge_report_system"

REM Show current directory for verification
echo Current directory: %CD%
echo.

REM List Python files to verify they exist
echo Python files in current directory:
dir *.py /b
echo.

REM Check if reportlab is installed
echo Checking dependencies...
python -c "import reportlab; print('reportlab is installed')" 2>nul || echo "reportlab is NOT installed - run: pip install reportlab"
python -c "import tkinter; print('tkinter is available')" 2>nul || echo "tkinter is NOT available"
echo.

REM Run the application
echo Launching Cambridge Report Card Generator...
python main.py

echo.
echo Application finished.
pause