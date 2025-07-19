# Markdown to eBook Converter

A comprehensive Python tool to convert markdown files into various eBook formats including EPUB, HTML, PDF, and combined Markdown.

## Features

- 📚 **Multiple Output Formats**: EPUB, HTML, PDF, and combined Markdown
- 🖼️ **Cover Image Support**: Automatically includes coverpage.png from the book folder
- 🎯 **Interactive Menu**: Choose output format via command line or interactive menu
- 📖 **Chapter Organization**: Automatically sorts chapters by filename
- 🌐 **Browser Preview**: HTML output opens automatically in your browser
- 📱 **Kindle Compatible**: EPUB format works with Kindle and other e-readers
- 🚀 **Easy Setup**: Run scripts for automatic environment setup

## Quick Start

### Windows (PowerShell)
```powershell
.\run_converter.ps1
```

### Linux/Mac (Bash)
```bash
chmod +x run_converter.sh
./run_converter.sh
```

These scripts will automatically:
- ✅ Create and activate virtual environment
- ✅ Install all dependencies
- ✅ Run the converter with interactive menu

## Manual Setup

1. **Create and activate a virtual environment:**
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

2. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

## Project Structure

```
your_project/
├── .venv/                    # Virtual environment
├── book/                     # Your markdown files and cover
│   ├── chapter_1_preface_and_intro.md
│   ├── chapter_2_extract_phase.md
│   ├── ... (all other chapters)
│   └── coverpage.png         # Cover image (optional)
├── ebook_converter.py        # Main converter script
├── run_converter.ps1         # Windows PowerShell run script
├── run_converter.sh          # Linux/Mac bash run script
├── requirements.txt          # Python dependencies
└── README.md               # This file
```

## Usage

### Interactive Mode (Recommended)
```powershell
python ebook_converter.py
```
This will show an interactive menu to choose your output format.

### Command Line Mode
```powershell
# Convert to EPUB
python ebook_converter.py -f epub -o my_book.epub

# Convert to HTML (opens in browser)
python ebook_converter.py -f html -o my_book.html

# Convert to PDF
python ebook_converter.py -f pdf -o my_book.pdf

# Convert to combined Markdown
python ebook_converter.py -f md -o my_book_combined.md

# Convert to all formats
python ebook_converter.py -f all -o my_book
```

## Output Formats

1. **EPUB**: eBook format compatible with Kindle, Kobo, and other e-readers
2. **HTML**: Web format with styling, automatically opens in browser
3. **PDF**: Portable Document Format with proper formatting
4. **Combined Markdown**: Single markdown file with all chapters
5. **All Formats**: Creates all four formats at once

## Configuration

Edit the configuration section in `ebook_converter.py` to customize:

```python
BOOK_TITLE = "Mastering ETL Pipelines for Data Science Workflows"
AUTHOR = "Pankaj Nagar"
LANGUAGE = "en"
IDENTIFIER = "urn:isbn:9780000000001"
PUBLISHER = "Independent Publishing"
```

## Notes

- Place all your markdown files in the `book/` folder
- Include `coverpage.png` in the `book/` folder for cover image support
- Files are processed in alphabetical order by filename
- HTML output includes responsive styling and opens automatically in your browser
- PDF includes proper chapter formatting and title pages
- Use the run scripts for the easiest setup experience

## Example

```powershell
# Quick start with run script
.\run_converter.ps1

# Or manual command line
python ebook_converter.py -f epub -o mastering_etl_pipelines.epub
```

This will create a Kindle-compatible EPUB file with your cover image and all chapters properly formatted. 