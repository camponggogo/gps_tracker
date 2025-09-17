@echo off
echo ============================================================
echo 🚗 GPS Vehicle Simulator - Windows Launcher
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
pip install aiohttp
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo 🚀 Starting vehicle simulator...
echo.
echo 📍 Make sure the GPS tracking server is running on port 17890
echo 🗺️  Open http://localhost:17890 to see the map
echo ⏹️  Press Ctrl+C to stop
echo ============================================================
echo.

python start_simulator.py

pause
