# IMPORTANT: Save this file as UTF-8 (no BOM) for best compatibility in PowerShell

Write-Host "Ebook Converter - PowerShell Script" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green


# Define the virtual environment path
$venvPath = ".venv"
$venvScripts = "$venvPath\Scripts"
$venvPython = "$venvScripts\python.exe"

# Check if the virtual environment exists and is Windows-compatible
if (-not (Test-Path $venvPython)) {
    if (Test-Path $venvPath) {
        Write-Host "Existing virtual environment is not Windows-compatible. Recreating..." -ForegroundColor Yellow
        Remove-Item $venvPath -Recurse -Force
    } else {
        Write-Host "Virtual environment not found. Creating one..." -ForegroundColor Yellow
    }
    python -m venv $venvPath
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to create virtual environment." -ForegroundColor Red
        exit 1
    }
    Write-Host "Virtual environment created." -ForegroundColor Green
}

# Activate the virtual environment (for user convenience)
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
. "$venvScripts\Activate.ps1"

# Always use the venv's python executable
$pythonPath = $venvPython
if (-not (Test-Path $pythonPath)) {
    Write-Host "Failed to find Python in virtual environment. Path: $pythonPath" -ForegroundColor Red
    exit 1
}
Write-Host "Virtual environment activated." -ForegroundColor Green

# Install dependencies if requirements.txt exists and dependencies are not already installed
if (Test-Path "requirements.txt") {
    Write-Host "Checking for Python dependencies..." -ForegroundColor Yellow
    $depsInstalled = $false
    try {
        & $pythonPath -c "import ebooklib" 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Dependencies already installed." -ForegroundColor Green
            $depsInstalled = $true
        }
    } catch {
        # Do nothing, will install below
    }
    if (-not $depsInstalled) {
        Write-Host "Dependencies not found or incomplete. Installing from requirements.txt..." -ForegroundColor Yellow
        & $pythonPath -m pip install -r requirements.txt
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Failed to install dependencies." -ForegroundColor Red
            exit 1
        }
        Write-Host "Dependencies installed." -ForegroundColor Green
    }
} else {
    Write-Host "requirements.txt not found. Skipping dependency installation." -ForegroundColor Yellow
}

# Check if book directory exists
if (-not (Test-Path "book")) {
    Write-Host "Book directory not found! Please create a 'book' folder with your markdown files." -ForegroundColor Red
    exit 1
}

# Check if ebook_converter.py exists
if (-not (Test-Path "ebook_converter.py")) {
    Write-Host "ebook_converter.py not found!" -ForegroundColor Red
    exit 1
}

# Run the ebook converter
Write-Host "Running ebook converter..." -ForegroundColor Green
& $pythonPath ebook_converter.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to run ebook_converter.py." -ForegroundColor Red
    exit 1
}
Write-Host "Conversion complete!" -ForegroundColor Green
Write-Host "Press Enter to exit..." -ForegroundColor Cyan
[void][System.Console]::ReadLine()