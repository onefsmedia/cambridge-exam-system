# Cambridge International Examination Report System

A modern, professional Python application for generating Cambridge International Examination report cards with advanced text wrapping, weighted grading, and professional PDF output.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-orange.svg)
![ReportLab](https://img.shields.io/badge/PDF-ReportLab-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

### 🎯 Core Functionality
- **175 Cambridge Subjects**: Complete database of Cambridge International subjects with official coefficients
- **Smart Text Wrapping**: Advanced UI and PDF text wrapping that prevents overflow and maintains professional appearance
- **Auto-Generated Candidate Numbers**: Unique ID generation (CB + Year + Random digits)
- **Intelligent Grade Calculation**: Automatic conversion of raw scores (0-100) to Cambridge grades (A* to G)
- **Weighted Averages**: Precise calculations using Cambridge's official coefficient system

### 🎨 Modern Interface
- **CustomTkinter GUI**: Modern, responsive interface with professional styling
- **Compact Column Design**: Optimized layout with abbreviated headers ("Coeff" instead of "Coefficient")
- **Dynamic Text Handling**: Subject names wrap intelligently without breaking words incorrectly
- **Real-time Preview**: Live updates as you input data

### 📄 Professional PDF Output
- **Compact Layout**: Optimized to fit most reports on a single A4 page
- **Multiple Font Sizes**: Reduced spacing and font sizes for maximum content density
- **Three Table System**: Student info, subject grades, and final summary tables
- **HTML Text Rendering**: Proper paragraph objects for clean text breaks

### ⚙️ Advanced Features
- **Editable Coefficients**: Settings dialog with live preview and validation
- **Subject Management**: Add, edit, and remove subjects with data validation
- **Teacher Comments**: Multi-line text input with proper wrapping
- **Email Integration**: Direct email sending capability
- **Cross-Platform**: Windows, macOS, and Linux support

## 🚀 Quick Start

### 🔥 Super Quick Setup (Recommended)

**Option 1: One-Click Setup (Windows)**
```bash
# Download and setup everything automatically
git clone https://github.com/onefsmedia/cambridge-exam-system.git
cd cambridge-exam-system
install.bat
run.bat
```

**Option 2: One-Click Setup (Mac/Linux)**
```bash
# Download and setup everything automatically
git clone https://github.com/onefsmedia/cambridge-exam-system.git
cd cambridge-exam-system
chmod +x install.sh run.sh
./install.sh
./run.sh
```

**Option 3: GitHub Codespaces (Browser)**
1. Click the green "Code" button on GitHub
2. Select "Codespaces" tab
3. Click "Create codespace on main"
4. Wait for setup, then run: `python main_gui_complete.py`

### 📋 Prerequisites
- Python 3.8 or higher
- Windows, macOS, or Linux

### 🛠️ Manual Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/onefsmedia/cambridge-exam-system.git
   cd cambridge-exam-system
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python main_gui_complete.py
   ```

## 📋 Requirements

See `requirements.txt` for full dependencies:
- `customtkinter` - Modern GUI framework
- `reportlab` - Professional PDF generation
- `Pillow` - Image processing support

## 🎓 Cambridge Subjects Database

The system includes 175+ Cambridge International subjects including:

**Core Subjects:**
- Mathematics (0580) - Coefficient: 2.0
- Additional Mathematics (4037) - Coefficient: 1.8
- Physics (0625) - Coefficient: 1.8
- Chemistry (0620) - Coefficient: 1.8
- Biology (0610) - Coefficient: 1.7

**Languages:**
- English Language (0500) - Coefficient: 2.0
- English Literature (0486) - Coefficient: 1.5
- Spanish (0530) - Coefficient: 1.4
- French (0520) - Coefficient: 1.4

**And many more...**

## 🖥️ User Interface

### Main Application Window
- **Subject Selection**: Multi-select interface with search/filter capabilities
- **Grade Input**: Intuitive score entry with automatic grade calculation
- **Comments Section**: Rich text input for teacher feedback
- **Live Preview**: Real-time weighted average calculations

### Features Showcase
- **Text Wrapping**: Long subject names like "Co-ordinated Sciences (Double Award)" wrap cleanly
- **Compact Design**: Abbreviated headers save space while maintaining clarity
- **Professional Layout**: Consistent with Cambridge International standards

## 📊 Grading System

### Grade Boundaries
| Score Range | Grade | Description |
|-------------|-------|-------------|
| 90-100      | A*    | Outstanding |
| 80-89       | A     | Excellent   |
| 70-79       | B     | Very Good   |
| 60-69       | C     | Good        |
| 50-59       | D     | Satisfactory|
| 40-49       | E     | Acceptable  |
| 30-39       | F     | Below Average|
| 0-29        | G     | Ungraded    |

### Weighted Calculation
Final grades are calculated using Cambridge's coefficient system:
```
Weighted Score = Raw Score × Subject Coefficient
Final Average = Total Weighted Score ÷ Total Coefficients
```

## 🗂️ Project Structure

```
cambridge-exam-system/
├── main_gui_complete.py    # Main application entry point
├── config.py              # Configuration and subjects database
├── pdf_generator.py       # Professional PDF generation
├── grade_calculator.py    # Grading logic and calculations
├── theme_manager.py       # UI theme management
├── requirements.txt       # Python dependencies
├── README.md             # Documentation
├── .gitignore           # Git ignore rules
└── reports/             # Generated PDF reports (auto-created)
```

## 🛠️ Configuration

### Adding New Subjects
Edit `config.py` and add to the `CAMBRIDGE_SUBJECTS` list:
```python
{
    "code": "XXXX",
    "name": "New Subject Name",
    "coefficient": 1.5
}
```

### Customizing PDF Layout
Modify `PDF_STYLE` in `config.py`:
```python
PDF_STYLE = {
    "title_font_size": 16,
    "header_font_size": 14,
    "body_font_size": 10,
    "small_font_size": 9,
    "line_height": 12
}
```

### UI Customization
Adjust column widths and text wrapping in `main_gui_complete.py`:
```python
header_widths = [170, 80, 60, 70, 250]  # Subject, Score, Grade, Coeff, Comments
wraplength = 160  # Text wrapping length
```

## 🐛 Troubleshooting

### Common Issues

**"Module not found" errors:**
```bash
pip install -r requirements.txt
```

**PDF generation fails:**
- Ensure ReportLab is properly installed
- Check file permissions in the reports directory

**Text wrapping issues:**
- Verify CustomTkinter version compatibility
- Check subject name lengths in config.py

**Application won't start:**
- Confirm Python 3.8+ is installed
- Activate virtual environment
- Check all dependencies are installed

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup
```bash
# Clone your fork
git clone https://github.com/yourusername/cambridge-exam-system.git
cd cambridge-exam-system

# Create development environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/  # If test suite exists
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏆 Acknowledgments

- Cambridge International for the grading standards and subject coefficients
- CustomTkinter team for the modern GUI framework
- ReportLab team for professional PDF generation capabilities
- Python community for excellent documentation and support

## 📧 Contact

For questions, suggestions, or support:
- Open an issue on GitHub
- Email: [your-email@example.com]
- Documentation: [Project Wiki](https://github.com/yourusername/cambridge-exam-system/wiki)

---

**Made with ❤️ for Cambridge International educators and students**

1. Mathematics (Coefficient: 2.0)
2. Physics (Coefficient: 1.8)
3. English Literature (Coefficient: 1.5)
4. Biology (Coefficient: 1.7)
5. History (Coefficient: 1.3)
6. Chemistry (Coefficient: 1.8)
7. Geography (Coefficient: 1.4)
8. Economics (Coefficient: 1.6)
9. Computer Science (Coefficient: 1.9)
10. Art & Design (Coefficient: 1.2)

## Grade Scale

- **A***: 90-100%
- **A**: 80-89%
- **B**: 70-79%
- **C**: 60-69%
- **D**: 50-59%
- **E**: 40-49%
- **F**: 30-39%
- **G**: 20-29%

## Installation

### Prerequisites

- Python 3.7 or higher
- tkinter (usually included with Python)

### Setup

1. **Clone or download the project files**
   ```bash
   # All files should be in the same directory:
   # cambridge_report_system/
   # ├── main.py
   # ├── main_gui.py
   # ├── config.py
   # ├── grade_calculator.py
   # ├── pdf_generator.py
   # ├── requirements.txt
   # └── README.md
   ```

2. **Install required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   Or install manually:
   ```bash
   pip install reportlab
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

## Usage

### Getting Started

1. **Launch the application**
   - Run `python main.py` from the command line
   - The GUI window will open with a welcome message

2. **Enter Student Information**
   - Student Name (required for PDF generation)
   - Candidate Number
   - Exam Session (defaults to current year)
   - School Name

3. **Add Subjects and Grades**
   - Select a subject from the dropdown menu (coefficient displays automatically)
   - Enter a raw score (0-100) - grade calculates automatically
   - Add teacher comments (optional)
   - Click "Add Subject" to add to the report
   - Use "Edit Selected Subject" to modify existing entries
   - Use "Remove Selected Subject" to delete entries

4. **Customize Settings** (Optional)
   - Click "Settings" to modify subject coefficients
   - View and edit coefficient values for each subject
   - Reset to default values if needed

5. **Review and Generate**
   - View all added subjects in the grades table
   - Check the final weighted average and grade
   - Click "Generate PDF Report" (bottom right) to create the report card

### Features Guide

#### Subject Management
- **Add Subjects**: Select from dropdown, enter score, add comments
- **Edit Subjects**: Select from table and click "Edit Selected Subject" to modify
- **Remove Subjects**: Select from the table and click "Remove Selected Subject"
- **Coefficient Settings**: Click "Settings" to modify subject coefficients

#### Auto-Generated Features
- **Candidate Numbers**: Automatically generated when creating new students (CB + Year + Random)
- **Grade Calculation**: Real-time calculation as scores are entered
- **Coefficient Display**: Automatic display when subjects are selected

#### Report Generation
- PDF files are saved in the `reports/` folder
- Filename format: `StudentName_Cambridge_Report_YYYYMMDD_HHMMSS.pdf`
- Click "View Reports Folder" to open the folder containing generated reports
- Generate button is positioned at the bottom right for easy access

#### Data Management
- **Clear All**: Removes all entered data (with confirmation)
- **Validation**: Application validates scores (must be 0-100) and prevents duplicate subjects

## File Structure

```
cambridge_report_system/
├── main.py              # Application entry point
├── main_gui.py          # GUI interface using tkinter
├── config.py            # Configuration (subjects, grades, settings)
├── grade_calculator.py  # Cambridge grading calculations
├── pdf_generator.py     # PDF report generation
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── reports/            # Generated PDF reports (created automatically)
```

## Customization

### Adding New Subjects
Edit `config.py` and add to the `CAMBRIDGE_SUBJECTS` list:
```python
{"name": "New Subject", "coefficient": 1.5}
```

### Modifying Grade Thresholds
Edit the `GRADE_THRESHOLDS` list in `config.py`:
```python
{"min": 85, "max": 100, "grade": "A*"}
```

### Changing PDF Layout
Modify the `PDF_STYLE` dictionary in `config.py` or edit the PDF generation functions in `pdf_generator.py`.

## Troubleshooting

### Common Issues

1. **"reportlab not found" error**
   ```bash
   pip install reportlab
   ```

2. **"tkinter not found" error (rare)**
   - On Ubuntu/Debian: `sudo apt-get install python3-tk`
   - On CentOS/RHEL: `sudo yum install tkinter`
   - On Windows/macOS: Reinstall Python from python.org

3. **Permission errors when saving PDFs**
   - Ensure write permissions in the application directory
   - Try running as administrator (Windows) or with sudo (Linux/macOS)

4. **PDF not generating**
   - Check that student name is entered
   - Ensure at least one subject is added
   - Check console output for error messages

### Error Messages

- **"Invalid range"**: Score must be between 0 and 100
- **"Select a subject"**: Choose a subject from the dropdown before adding
- **"Student name required"**: Enter a student name to generate reports
- **"No subjects added"**: Add at least one subject before generating

## Technical Details

### Dependencies
- **reportlab**: PDF generation library
- **tkinter**: GUI framework (included with Python)
- **datetime**: Date/time handling (built-in)
- **os**: File system operations (built-in)

### Calculations
The final grade is calculated using Cambridge's weighted average system:
```
Final Average = (Σ(Score × Coefficient)) / (Σ(Coefficient))
```

Example:
- Mathematics: 85 × 2.0 = 170.0
- Physics: 78 × 1.8 = 140.4
- Total: 310.4 ÷ 3.8 = 81.7% (Grade A)

## License

This project is for educational purposes. Please ensure compliance with Cambridge International examination policies when using this tool.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify all files are in the correct directory
3. Ensure all dependencies are installed
4. Check the console output for error messages

## Version History

- **v1.0.0**: Initial release with full Cambridge grading system support