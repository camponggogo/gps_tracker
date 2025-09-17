@echo off
echo ============================================================
echo 🐍 GPS Area Tracking System - Virtual Environment Setup
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
echo 🐍 Creating virtual environment...
if exist "venv" (
    echo ⚠️  Virtual environment already exists
    echo 🔄 Removing old virtual environment...
    rmdir /s /q venv
)

python -m venv venv
if %errorlevel% neq 0 (
    echo ❌ Failed to create virtual environment
    pause
    exit /b 1
)

echo ✅ Virtual environment created successfully!
echo.
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo 📦 Upgrading pip...
python -m pip install --upgrade pip

echo.
echo 📦 Installing dependencies...
pip install fastapi==0.104.1
pip install uvicorn==0.24.0
pip install sqlalchemy==2.0.23
pip install pymysql==1.1.0
pip install python-multipart==0.0.6
pip install python-jose[cryptography]==3.3.0
pip install passlib[bcrypt]==1.7.4
pip install python-dotenv==1.0.0
pip install pydantic==2.5.0
pip install pydantic-settings==2.1.0
pip install httpx==0.25.2
pip install jinja2==3.1.2
pip install aiofiles==23.2.1
pip install python-dateutil==2.8.2
pip install pytz==2023.3
pip install requests==2.31.0

if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ✅ Dependencies installed successfully!
echo.
echo 🗄️  Setting up database...
python setup_mariadb.py
if %errorlevel% neq 0 (
    echo ❌ Database setup failed
    pause
    exit /b 1
)

echo.
echo 🎉 Setup completed successfully!
echo.
echo 📋 To use the system:
echo    1. Run: activate_venv.bat
echo    2. Run: python run.py
echo.
echo 🚀 Or run everything at once: run_with_venv.bat
echo.

pause
