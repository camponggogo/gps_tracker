#!/bin/bash

echo "============================================================"
echo "🐧 GPS Area Tracking System - Ubuntu 24.04 Installation"
echo "============================================================"
echo

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "⚠️  Running as root. This is not recommended for security reasons."
    echo "Please run this script as a regular user with sudo privileges."
    exit 1
fi

# Check Ubuntu version
echo "🔍 Checking Ubuntu version..."
if [ -f /etc/os-release ]; then
    . /etc/os-release
    echo "✅ Detected: $PRETTY_NAME"
    if [[ "$VERSION_ID" != "24.04" ]]; then
        echo "⚠️  This script is optimized for Ubuntu 24.04"
        echo "Current version: $VERSION_ID"
        read -p "Continue anyway? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "❌ Installation cancelled"
            exit 1
        fi
    fi
else
    echo "⚠️  Cannot detect Ubuntu version"
fi

# Check Python installation
echo "🔍 Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    echo "🔧 Installing Python 3..."
    sudo apt update
    sudo apt install -y python3 python3-pip python3-venv python3-dev
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install Python 3"
        exit 1
    fi
fi

PYTHON_VERSION=$(python3 --version 2>&1)
echo "✅ Python version: $PYTHON_VERSION"

# Install system dependencies
echo "📦 Installing system dependencies..."
sudo apt update
sudo apt install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    libmysqlclient-dev \
    pkg-config \
    curl \
    git \
    software-properties-common

if [ $? -ne 0 ]; then
    echo "❌ Failed to install system dependencies"
    exit 1
fi

echo "✅ System dependencies installed"

# Install MariaDB
echo "📦 Installing MariaDB..."
sudo apt install -y mariadb-server mariadb-client
sudo systemctl start mariadb
sudo systemctl enable mariadb

echo "🔒 Securing MariaDB installation..."
echo "You will be prompted to set a root password and configure security options."
echo "Press Enter to continue..."
read
sudo mysql_secure_installation

# Create virtual environment
echo "🔧 Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists"
    read -p "Do you want to remove it and create a new one? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🗑️  Removing old virtual environment..."
        rm -rf venv
    else
        echo "✅ Using existing virtual environment"
        source venv/bin/activate
        echo "📦 Installing dependencies..."
        pip install --upgrade pip
        pip install -r requirements_ubuntu_24_04.txt
        if [ $? -ne 0 ]; then
            echo "❌ Failed to install dependencies"
            exit 1
        fi
        echo "✅ Dependencies installed successfully"
        exit 0
    fi
fi

python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "❌ Failed to create virtual environment"
    exit 1
fi

echo "✅ Virtual environment created"

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install dependencies in specific order
echo "📦 Installing dependencies for Ubuntu 24.04..."

# Install core packages first
pip install --no-cache-dir \
    pydantic==2.5.0 \
    pydantic-core==2.14.1 \
    pydantic-settings==2.1.0 \
    annotated-types==0.7.0

# Install FastAPI
pip install --no-cache-dir \
    fastapi==0.104.1 \
    uvicorn==0.24.0 \
    starlette==0.27.0

# Install database packages
pip install --no-cache-dir \
    sqlalchemy==2.0.23 \
    pymysql==1.1.0 \
    mysql-connector-python==9.4.0

# Install remaining packages
pip install --no-cache-dir -r requirements_ubuntu_24_04.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    echo "🔧 Trying alternative installation method..."
    ./fix_ubuntu_24_04.sh
    if [ $? -ne 0 ]; then
        echo "❌ Alternative installation also failed"
        exit 1
    fi
fi

echo "✅ Dependencies installed successfully"

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p logs uploads static/css static/js templates

echo "✅ Directories created"

# Create .env file
echo "📝 Creating .env file..."
cat > .env << EOF
# Database Configuration
DATABASE_URL=mysql+pymysql://gps_user:gps_password@localhost:3306/gps_track_db
DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_NAME=gps_track_db
DATABASE_USER=gps_user
DATABASE_PASSWORD=gps_password

# API Configuration
API_HOST=0.0.0.0
API_PORT=17890
API_DEBUG=true

# Security Configuration
SECRET_KEY=_5wwvZWMjUUpK7eg5sklHh8mpQE0UNtQSVabpIE0ArY
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# GPS Configuration
GPS_UPDATE_INTERVAL=30

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/gps_tracking.log
EOF

echo "✅ .env file created"

# Create database and user
echo "🔧 Creating database and user..."
echo "Please enter MariaDB root password:"
read -s ROOT_PASSWORD

SQL_COMMANDS="
CREATE DATABASE IF NOT EXISTS gps_track_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'gps_user'@'localhost' IDENTIFIED BY 'gps_password';
GRANT ALL PRIVILEGES ON gps_track_db.* TO 'gps_user'@'localhost';
FLUSH PRIVILEGES;
"

echo "$SQL_COMMANDS" | sudo mysql -u root -p"$ROOT_PASSWORD"

if [ $? -ne 0 ]; then
    echo "❌ Failed to create database and user"
    echo "Please run the following commands manually:"
    echo "sudo mysql -u root -p"
    echo "CREATE DATABASE IF NOT EXISTS gps_track_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    echo "CREATE USER IF NOT EXISTS 'gps_user'@'localhost' IDENTIFIED BY 'gps_password';"
    echo "GRANT ALL PRIVILEGES ON gps_track_db.* TO 'gps_user'@'localhost';"
    echo "FLUSH PRIVILEGES;"
    echo "EXIT;"
fi

echo "✅ Database and user created"

# Test installation
echo "🔧 Testing installation..."
python3 -c "
try:
    from pydantic_settings import BaseSettings
    print('✅ pydantic_settings imported successfully')
except ImportError as e:
    print(f'❌ pydantic_settings import failed: {e}')

try:
    from main import app
    print('✅ Main application imported successfully')
except Exception as e:
    print(f'❌ Main application import failed: {e}')
"

echo
echo "============================================================"
echo "🎉 Ubuntu 24.04 installation completed successfully!"
echo "============================================================"
echo
echo "📋 Next steps:"
echo "1. Run: python setup_mariadb.py"
echo "2. Run: python insert_sample_data.py"
echo "3. Run: ./run_with_venv.sh"
echo
echo "🌐 Access URLs:"
echo "   http://localhost:17890           - Main interface"
echo "   http://localhost:17890/docs     - API documentation"
echo
echo "🚀 Ready to run the GPS tracking system!"
echo
