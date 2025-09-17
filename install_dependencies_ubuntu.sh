#!/bin/bash

echo "============================================================"
echo "📦 GPS Area Tracking System - Dependencies Installer for Ubuntu"
echo "============================================================"
echo

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "⚠️  Running as root. This is not recommended for security reasons."
    echo "Please run this script as a regular user with sudo privileges."
    exit 1
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

# Check pip installation
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed"
    echo "🔧 Installing pip3..."
    sudo apt install -y python3-pip
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install pip3"
        exit 1
    fi
fi

echo "✅ pip3 is installed"

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
    git

if [ $? -ne 0 ]; then
    echo "❌ Failed to install system dependencies"
    exit 1
fi

echo "✅ System dependencies installed"

# Check if virtual environment exists
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
        echo "📦 Upgrading pip..."
        pip install --upgrade pip
        echo "📦 Installing Python dependencies..."
        pip install -r requirements.txt
        if [ $? -ne 0 ]; then
            echo "❌ Failed to install Python dependencies"
            exit 1
        fi
        echo "✅ Dependencies installed successfully"
        exit 0
    fi
fi

# Create virtual environment
echo "🔧 Creating virtual environment..."
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
pip install --upgrade pip

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install Python dependencies"
    echo "💡 Try running: pip install --upgrade pip"
    exit 1
fi

echo "✅ Python dependencies installed successfully"

# Install additional dependencies for simulator
echo "📦 Installing simulator dependencies..."
pip install aiohttp

if [ $? -ne 0 ]; then
    echo "⚠️  Failed to install simulator dependencies"
    echo "You can install them later with: pip install aiohttp"
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p logs uploads static/css static/js templates

echo "✅ Directories created"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    if [ -f "env.example" ]; then
        echo "📝 Creating .env file from env.example..."
        cp env.example .env
        echo "✅ Created .env file"
        echo "📝 Please edit .env file with your database settings"
    else
        echo "⚠️  env.example file not found"
    fi
else
    echo "✅ .env file already exists"
fi

echo
echo "============================================================"
echo "🎉 Dependencies installation completed successfully!"
echo "============================================================"
echo
echo "📋 Next steps:"
echo "1. Install MariaDB: ./install_mariadb_ubuntu.sh"
echo "2. Setup database: python setup_mariadb.py"
echo "3. Insert sample data: python insert_sample_data.py"
echo "4. Run the system: ./run_with_venv.sh"
echo
echo "🌐 Access URLs:"
echo "   http://localhost:17890           - Main interface"
echo "   http://localhost:17890/docs     - API documentation"
echo
echo "🚀 Ready to run the GPS tracking system!"
echo
