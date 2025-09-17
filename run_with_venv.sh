#!/bin/bash

echo "============================================================"
echo "🚗 GPS Area Tracking System - Run with Virtual Environment"
echo "============================================================"
echo

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "🔧 Creating virtual environment..."
    ./setup_venv.sh
    if [ $? -ne 0 ]; then
        echo "❌ Setup failed"
        exit 1
    fi
fi

echo "🔧 Activating virtual environment..."
source venv/bin/activate

echo "✅ Virtual environment activated!"

echo
echo "🚀 Starting GPS Area Tracking System..."
echo
echo "📍 Server will be available at: http://localhost:17890"
echo "📚 API Documentation: http://localhost:17890/docs"
echo "🗺️  Map Interface: http://localhost:17890"
echo
echo "⏹️  Press Ctrl+C to stop the server"
echo "============================================================"
echo

python run.py

echo
echo "👋 System stopped"
read -p "Press Enter to exit: "
