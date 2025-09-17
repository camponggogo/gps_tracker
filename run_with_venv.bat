@echo off
echo ============================================================
echo 🚗 GPS Area Tracking System - Run with Virtual Environment
echo ============================================================
echo.

if not exist "venv" (
    echo ❌ Virtual environment not found!
    echo 🔧 Creating virtual environment...
    call setup_venv.bat
    if %errorlevel% neq 0 (
        echo ❌ Setup failed
        pause
        exit /b 1
    )
)

echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

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
