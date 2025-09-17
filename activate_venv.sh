#!/bin/bash

echo "============================================================"
echo "🚗 GPS Area Tracking System - Activate Virtual Environment"
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
echo "📋 Available commands:"
echo "   python run.py                    - Run the system"
echo "   python run_with_simulator.py     - Run with simulator"
echo "   python setup_mariadb.py          - Setup database"
echo "   python insert_sample_data.py     - Insert sample data"
echo "   python view_sample_data.py       - View database data"
echo "   python test_system.py            - Test API endpoints"
echo
echo "🌐 Access URLs:"
echo "   http://localhost:17890           - Main interface"
echo "   http://localhost:17890/docs      - API documentation"
echo "   http://localhost:17890/health    - Health check"
echo
echo "⏹️  Type 'deactivate' to exit virtual environment"
echo "============================================================"
echo

# Start bash shell with activated environment
bash
