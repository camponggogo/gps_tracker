@echo off
echo ============================================================
echo 📦 GPS Area Tracking System - Dependencies Installer
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
echo 📦 Installing core dependencies...
pip install --upgrade pip
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
    echo ❌ Failed to install core dependencies
    pause
    exit /b 1
)

echo.
echo ✅ Core dependencies installed successfully!
echo.
echo 📋 Optional packages for advanced features:
echo    - folium (for advanced mapping)
echo    - geopandas (for geospatial analysis)
echo    - pandas (for data analysis)
echo    - numpy (for numerical computing)
echo.
echo 💡 To install optional packages, run:
echo    pip install folium geopandas pandas numpy matplotlib
echo.
echo 🚀 Ready to run the GPS tracking system!
echo.

pause
