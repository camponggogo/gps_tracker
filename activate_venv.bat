@echo off
echo ============================================================
echo 🐍 Activating Virtual Environment
echo ============================================================
echo.

if not exist "venv" (
    echo ❌ Virtual environment not found!
    echo Please run setup_venv.bat first
    pause
    exit /b 1
)

echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

echo ✅ Virtual environment activated!
echo.
echo 📋 You can now run:
echo    python run.py
echo    python test_system.py
echo    python simulator/start_simulator.py
echo.
echo 💡 To deactivate, type: deactivate
echo.

cmd /k
