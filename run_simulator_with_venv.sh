#!/bin/bash

echo "============================================================"
echo "🚗 GPS Area Tracking System + Simulator - Run with Virtual Environment"
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

echo
echo "📦 Installing simulator dependencies..."
pip install aiohttp

echo
echo "🚀 Starting GPS Area Tracking System with Vehicle Simulator..."
echo
echo "📍 Server will be available at: http://localhost:17890"
echo "📚 API Documentation: http://localhost:17890/docs"
echo "🗺️  Map Interface: http://localhost:17890"
echo "🚗 10 vehicles will start sending GPS data automatically"
echo
echo "⏹️  Press Ctrl+C to stop everything"
echo "============================================================"
echo

python run_with_simulator.py

echo
echo "👋 System stopped"
read -p "Press Enter to exit: "
