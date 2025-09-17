@echo off
echo ============================================================
echo 🚗 GPS Area Tracking System - Windows Startup Script
echo ============================================================
echo.

echo 🔍 Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

echo.
echo 📦 Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo 🗄️  Setting up database...
python setup_mariadb.py
if %errorlevel% neq 0 (
    echo ❌ Database setup failed
    pause
    exit /b 1
)

echo.
echo 🚀 Starting GPS Area Tracking System...
echo.
echo 📍 Server will be available at: http://localhost:17890
echo 📚 API Documentation: http://localhost:17890/docs
echo 🗺️  Map Interface: http://localhost:17890
echo.
echo ⏹️  Press Ctrl+C to stop the server
echo ============================================================
echo.

python run.py

pause
