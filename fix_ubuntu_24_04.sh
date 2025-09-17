#!/bin/bash

echo "============================================================"
echo "🔧 Fix Ubuntu 24.04 Dependencies Issues"
echo "============================================================"
echo

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
fi

echo "🔧 Activating virtual environment..."
source venv/bin/activate

echo "📦 Upgrading pip..."
pip install --upgrade pip

echo "📦 Installing system dependencies..."
sudo apt update
sudo apt install -y \
    python3-dev \
    python3-venv \
    build-essential \
    libssl-dev \
    libffi-dev \
    libmysqlclient-dev \
    pkg-config

echo "📦 Installing core dependencies first..."
pip install --no-cache-dir \
    setuptools \
    wheel \
    pip-tools

echo "📦 Installing pydantic and related packages..."
pip install --no-cache-dir \
    pydantic==2.5.0 \
    pydantic-core==2.14.1 \
    pydantic-settings==2.1.0 \
    annotated-types==0.7.0

echo "📦 Installing FastAPI and related packages..."
pip install --no-cache-dir \
    fastapi==0.104.1 \
    uvicorn==0.24.0 \
    starlette==0.27.0 \
    anyio==3.7.1

echo "📦 Installing database packages..."
pip install --no-cache-dir \
    sqlalchemy==2.0.23 \
    pymysql==1.1.0 \
    greenlet==3.2.4

echo "📦 Installing authentication packages..."
pip install --no-cache-dir \
    python-jose[cryptography]==3.3.0 \
    passlib[bcrypt]==1.7.4 \
    cryptography==46.0.1 \
    bcrypt==4.3.0

echo "📦 Installing utility packages..."
pip install --no-cache-dir \
    python-dotenv==1.0.0 \
    python-multipart==0.0.6 \
    httpx==0.25.2 \
    jinja2==3.1.2 \
    aiofiles==23.2.1 \
    python-dateutil==2.8.2 \
    pytz==2023.3 \
    requests==2.31.0

echo "📦 Installing additional packages..."
pip install --no-cache-dir \
    mysql-connector-python \
    aiohttp

echo "🔧 Testing imports..."
python3 -c "
try:
    from pydantic_settings import BaseSettings
    print('✅ pydantic_settings imported successfully')
except ImportError as e:
    print(f'❌ pydantic_settings import failed: {e}')

try:
    from fastapi import FastAPI
    print('✅ fastapi imported successfully')
except ImportError as e:
    print(f'❌ fastapi import failed: {e}')

try:
    from sqlalchemy import create_engine
    print('✅ sqlalchemy imported successfully')
except ImportError as e:
    print(f'❌ sqlalchemy import failed: {e}')

try:
    import pymysql
    print('✅ pymysql imported successfully')
except ImportError as e:
    print(f'❌ pymysql import failed: {e}')
"

echo "🔧 Testing main application..."
python3 -c "
try:
    from main import app
    print('✅ Main application imported successfully')
except Exception as e:
    print(f'❌ Main application import failed: {e}')
"

echo
echo "============================================================"
echo "🎉 Dependencies fix completed!"
echo "============================================================"
echo
echo "📋 Next steps:"
echo "1. Run: python setup_mariadb.py"
echo "2. Run: python insert_sample_data.py"
echo "3. Run: ./run_with_venv.sh"
echo
echo "🚀 Ready to run the GPS tracking system!"
echo
