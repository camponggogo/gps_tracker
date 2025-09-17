# GPS Area Tracking System - Virtual Environment Setup (PowerShell)
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🐍 GPS Area Tracking System - Virtual Environment Setup" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "🔍 Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ and try again" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "🐍 Creating virtual environment..." -ForegroundColor Yellow

# Remove existing venv if it exists
if (Test-Path "venv") {
    Write-Host "⚠️  Virtual environment already exists" -ForegroundColor Yellow
    Write-Host "🔄 Removing old virtual environment..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force "venv"
}

# Create virtual environment
try {
    python -m venv venv
    Write-Host "✅ Virtual environment created successfully!" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to create virtual environment" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Yellow

# Activate virtual environment
try {
    & "venv\Scripts\Activate.ps1"
    Write-Host "✅ Virtual environment activated!" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to activate virtual environment" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "📦 Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

Write-Host ""
Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow

# Install dependencies
$packages = @(
    "fastapi==0.104.1",
    "uvicorn==0.24.0",
    "sqlalchemy==2.0.23",
    "pymysql==1.1.0",
    "python-multipart==0.0.6",
    "python-jose[cryptography]==3.3.0",
    "passlib[bcrypt]==1.7.4",
    "python-dotenv==1.0.0",
    "pydantic==2.5.0",
    "pydantic-settings==2.1.0",
    "httpx==0.25.2",
    "jinja2==3.1.2",
    "aiofiles==23.2.1",
    "python-dateutil==2.8.2",
    "pytz==2023.3",
    "requests==2.31.0"
)

foreach ($package in $packages) {
    Write-Host "Installing $package..." -ForegroundColor Yellow
    pip install $package
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install $package" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host ""
Write-Host "✅ Dependencies installed successfully!" -ForegroundColor Green

Write-Host ""
Write-Host "🗄️  Setting up database..." -ForegroundColor Yellow
python setup_mariadb.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Database setup failed" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "🎉 Setup completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 To use the system:" -ForegroundColor Cyan
Write-Host "   1. Run: .\activate_venv.ps1" -ForegroundColor White
Write-Host "   2. Run: python run.py" -ForegroundColor White
Write-Host ""
Write-Host "🚀 Or run everything at once: .\run_with_venv.ps1" -ForegroundColor Cyan
Write-Host ""

Read-Host "Press Enter to exit"
