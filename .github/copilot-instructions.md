# Word to PDF Converter - Project Instructions

## Project Overview
Windows uygulaması - Word (.docx) dosyalarını PDF formatına dönüştürün

## Technology Stack
- Language: Python 3.8+
- GUI Framework: Tkinter
- PDF Generation: ReportLab
- Document Parsing: python-docx
- Platform: Windows 7+

## Project Setup Status

- [x] Verify that the copilot-instructions.md file in the .github directory is created.
- [x] Clarify Project Requirements
- [x] Scaffold the Project
- [x] Customize the Project
- [x] Install Required Extensions
- [x] Compile the Project
- [x] Create and Run Task
- [x] Launch the Project
- [x] Ensure Documentation is Complete

## Installation & Running

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Application
```bash
python run.py
```

## Project Structure
```
pdf-cevirici/
├── run.py                 # Main entry point
├── requirements.txt       # Python dependencies
├── README.md             # Documentation
├── src/
│   ├── gui.py           # GUI interface
│   └── converter.py      # Conversion engine
└── .vscode/
    └── settings.json     # VS Code settings
```

## Key Features
- Simple and user-friendly interface
- Quick Word to PDF conversion
- Auto-save to Downloads folder
- Turkish language support
- Status monitoring

## Development Notes
- All converted files are saved to the user's Downloads folder
- If a file with the same name exists, a number suffix is added
- The application provides option to open the converted PDF
- Error handling for invalid files and conversion issues
