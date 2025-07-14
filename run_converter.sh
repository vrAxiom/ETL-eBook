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
    print_success "Python found: $(python3 --version)"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    print_success "Python found: $(python --version)"
else
    print_error "Python not found! Please install Python first."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    print_info "Creating virtual environment..."
    $PYTHON_CMD -m venv .venv
    if [ $? -ne 0 ]; then
        print_error "Failed to create virtual environment!"
        exit 1
    fi
    print_success "Virtual environment created"
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source .venv/bin/activate
if [ $? -ne 0 ]; then
    print_error "Failed to activate virtual environment!"
    exit 1
fi
print_success "Virtual environment activated"

# Check if requirements.txt exists
if [ -f "requirements.txt" ]; then
    print_info "Installing dependencies..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        print_error "Failed to install dependencies!"
        exit 1
    fi
    print_success "Dependencies installed"
else
    print_warning "requirements.txt not found, installing basic dependencies..."
    pip install markdown pypandoc ebooklib fpdf
    if [ $? -ne 0 ]; then
        print_error "Failed to install dependencies!"
        exit 1
    fi
    print_success "Basic dependencies installed"
fi

# Check if book directory exists
if [ ! -d "book" ]; then
    print_error "Book directory not found!"
    echo "Please create a 'book' folder with your markdown files."
    exit 1
fi

# Check if ebook_converter.py exists
if [ ! -f "ebook_converter.py" ]; then
    print_error "ebook_converter.py not found!"
    exit 1
fi

echo "🚀 Starting ebook converter..."
echo "====================================="

# Run the converter
$PYTHON_CMD ebook_converter.py

echo "====================================="
print_success "Conversion complete!"
echo "Press Enter to exit..."
read 