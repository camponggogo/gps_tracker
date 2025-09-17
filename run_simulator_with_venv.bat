@echo off
echo ============================================================
echo 🚗 GPS Area Tracking System + Simulator - Run with Virtual Environment
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
echo 📦 Installing simulator dependencies...
pip install aiohttp

echo.
echo 🚀 Starting GPS Area Tracking System with Vehicle Simulator...
echo.
echo 📍 Server will be available at: http://localhost:17890
echo 📚 API Documentation: http://localhost:17890/docs
echo 🗺️  Map Interface: http://localhost:17890
echo 🚗 10 vehicles will start sending GPS data automatically
echo.
echo ⏹️  Press Ctrl+C to stop everything
echo ============================================================
echo.

python run_with_simulator.py

pause
