#!/bin/bash

echo "============================================================"
echo "🚗 GPS Area Tracking System - Virtual Environment Setup"
echo "============================================================"
echo

# Check Python installation
echo "🔍 Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1)
echo "✅ Python version: $PYTHON_VERSION"

# Check if virtual environment already exists
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists"
    read -p "Do you want to remove it and create a new one? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🗑️  Removing old virtual environment..."
        rm -rf venv
    else
        echo "✅ Using existing virtual environment"
        exit 0
    fi
fi

echo "🔧 Creating virtual environment..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "❌ Failed to create virtual environment"
    exit 1
fi

echo "✅ Virtual environment created successfully"

echo "🔧 Activating virtual environment..."
source venv/bin/activate

echo "📦 Upgrading pip..."
pip install --upgrade pip

echo "📦 Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    echo "💡 Try running: pip install --upgrade pip"
    exit 1
fi

echo "✅ Dependencies installed successfully"

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

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p logs uploads static/css static/js templates

echo "✅ Directories created"

echo
echo "============================================================"
echo "🎉 Virtual environment setup completed successfully!"
echo "============================================================"
echo
echo "📋 Next steps:"
echo "1. Edit .env file with your database settings"
echo "2. Run the system: ./run_with_venv.sh"
echo "3. Open browser: http://localhost:17890"
echo "4. API docs: http://localhost:17890/docs"
echo
echo "🚀 Ready to track GPS data!"
echo
