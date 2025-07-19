#!/bin/bash

# Bash Script to Run Ebook Converter
# This script activates the virtual environment, installs dependencies, and runs the converter

echo "📚 Ebook Converter - Bash Script"
echo "====================================="

# Function to print colored output
print_success() {
    echo -e "\033[32m✅ $1\033[0m"
}

print_warning() {
    echo -e "\033[33m⚠️  $1\033[0m"
}

print_error() {
    echo -e "\033[31m❌ $1\033[0m"
}

print_info() {
    echo -e "\033[36m🔧 $1\033[0m"
}

# Check if Python is installed
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    print_success "Python found: $($PYTHON_CMD --version)"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    print_success "Python found: $($PYTHON_CMD --version)"
else
    print_error "Python not found! Please install Python first."
    exit 1
fi

# Define venv path
VENV_PATH=".venv"

# Check if virtual environment exists, if not, create it
if [ ! -d "$VENV_PATH" ]; then
    print_info "Virtual environment not found. Creating one..."
    $PYTHON_CMD -m venv $VENV_PATH
    if [ $? -ne 0 ]; then
        print_error "Failed to create virtual environment."
        exit 1
    fi
    print_success "Virtual environment created."
fi

# Activate virtual environment
print_info "Activating virtual environment..."
if [ -f "$VENV_PATH/bin/activate" ]; then
    # Unix-like venv
    # shellcheck disable=SC1091
    source "$VENV_PATH/bin/activate"
elif [ -f "$VENV_PATH/Scripts/activate" ]; then
    # Windows-style venv (sometimes created on macOS with certain Python installs)
    # shellcheck disable=SC1091
    source "$VENV_PATH/Scripts/activate"
else
    print_error "Could not find the virtual environment activation script!"
    exit 1
fi
if [ $? -ne 0 ]; then
    print_error "Failed to activate virtual environment!"
    exit 1
fi
print_success "Virtual environment activated."

# Use python from venv
if [ -f "$VENV_PATH/bin/python" ]; then
    PYTHON_CMD="$VENV_PATH/bin/python"
elif [ -f "$VENV_PATH/Scripts/python" ] && [ -x "$VENV_PATH/Scripts/python" ]; then
    PYTHON_CMD="$VENV_PATH/Scripts/python"
else
    print_error "Could not find a usable python executable in the virtual environment!"
    exit 1
fi

# Check if requirements.txt exists and dependencies are installed
if [ -f "requirements.txt" ]; then
    print_info "Checking for Python dependencies..."
    $PYTHON_CMD -c "import ebooklib" 2>/dev/null
    if [ $? -eq 0 ]; then
        print_success "Dependencies already installed."
    else
        print_info "Dependencies not found or incomplete. Installing from requirements.txt..."
        $PYTHON_CMD -m pip install -r requirements.txt
        if [ $? -ne 0 ]; then
            print_error "Failed to install dependencies."
            exit 1
        fi
        print_success "Dependencies installed."
    fi
else
    print_warning "requirements.txt not found. Skipping dependency installation."
fi

# Check if book directory exists
if [ ! -d "book" ]; then
    print_error "Book directory not found! Please create a 'book' folder with your markdown files."
    exit 1
fi

# Check if ebook_converter.py exists
if [ ! -f "ebook_converter.py" ]; then
    print_error "ebook_converter.py not found!"
    exit 1
fi

echo "🚀 Running ebook converter..."
$PYTHON_CMD ebook_converter.py
if [ $? -ne 0 ]; then
    print_error "Failed to run ebook_converter.py."
    exit 1
fi
print_success "Conversion complete!"
echo "Press Enter to exit..."
read 