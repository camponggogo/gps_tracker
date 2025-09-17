#!/usr/bin/env python3
"""
GPS Area Tracking System - Run Script
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version}")

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'pymysql',
        'pydantic',
        'dotenv'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Install missing packages:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    print("✅ All required packages are installed")

def check_environment():
    """Check environment configuration"""
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  .env file not found")
        print("📝 Copy env.example to .env and configure:")
        print("   cp env.example .env")
        print("   # Edit .env with your database settings")
        return False
    
    print("✅ Environment file found")
    return True

def create_directories():
    """Create necessary directories"""
    directories = ['logs', 'uploads']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    print("✅ Directories created")

def run_database_setup():
    """Run database setup if needed"""
    try:
        from database.database import test_db_connection, init_db
        
        if test_db_connection():
            print("✅ Database connection successful")
            init_db()
            print("✅ Database tables created")
        else:
            print("❌ Database connection failed")
            print("🔧 Please check your database configuration in .env")
            return False
    except Exception as e:
        print(f"❌ Database setup error: {e}")
        return False
    
    return True

def start_server():
    """Start the FastAPI server"""
    print("\n🚀 Starting GPS Area Tracking System...")
    print("📍 Server will be available at: http://localhost:17890")
    print("📚 API Documentation: http://localhost:17890/docs")
    print("🗺️  Map Interface: http://localhost:17890")
    print("\n⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        import uvicorn
        from config.settings import settings
        
        uvicorn.run(
            "main:app",
            host=settings.api_host,
            port=settings.api_port,
            reload=settings.api_debug,
            log_level=settings.log_level.lower()
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        sys.exit(1)

def main():
    """Main function"""
    print("=" * 60)
    print("🚗 GPS Area Tracking System")
    print("=" * 60)
    
    # Check system requirements
    check_python_version()
    check_dependencies()
    
    # Setup
    create_directories()
    
    if not check_environment():
        print("\n⚠️  Please configure .env file before running")
        sys.exit(1)
    
    # Database setup
    if not run_database_setup():
        print("\n❌ Database setup failed")
        sys.exit(1)
    
    # Start server
    start_server()

if __name__ == "__main__":
    main()
