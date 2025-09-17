#!/usr/bin/env python3
"""
GPS Area Tracking System - Setup Script
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def install_dependencies():
    """Install Python dependencies"""
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        print("❌ Failed to install dependencies")
        print("💡 Try running: pip install --upgrade pip")
        return False
    return True

def setup_environment():
    """Setup environment file"""
    env_file = Path(".env")
    env_example = Path("env.example")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if env_example.exists():
        shutil.copy(env_example, env_file)
        print("✅ Created .env file from env.example")
        print("📝 Please edit .env file with your database settings")
        return True
    else:
        print("❌ env.example file not found")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ['logs', 'uploads', 'static/css', 'static/js', 'templates']
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Created necessary directories")
    return True

def check_database_connection():
    """Check if database connection works"""
    try:
        from database.database import test_db_connection
        if test_db_connection():
            print("✅ Database connection successful")
            return True
        else:
            print("❌ Database connection failed")
            print("🔧 Please check your database configuration in .env")
            return False
    except Exception as e:
        print(f"❌ Database check error: {e}")
        print("🔧 Please install PostgreSQL and configure .env")
        return False

def initialize_database():
    """Initialize database tables"""
    try:
        from database.database import init_db
        init_db()
        print("✅ Database tables created")
        return True
    except Exception as e:
        print(f"❌ Database initialization error: {e}")
        return False

def main():
    """Main setup function"""
    print("=" * 60)
    print("🚗 GPS Area Tracking System - Setup")
    print("=" * 60)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    
    print(f"✅ Python version: {sys.version}")
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Setup environment
    if not setup_environment():
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        sys.exit(1)
    
    # Check database connection
    if not check_database_connection():
        print("\n⚠️  Database connection failed")
        print("📝 Please configure your database settings in .env file")
        print("🔧 Make sure PostgreSQL is running and accessible")
        sys.exit(1)
    
    # Initialize database
    if not initialize_database():
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("🎉 Setup completed successfully!")
    print("=" * 60)
    print("\n📋 Next steps:")
    print("1. Edit .env file with your database settings")
    print("2. Run the system: python run.py")
    print("3. Open browser: http://localhost:17890")
    print("4. API docs: http://localhost:17890/docs")
    print("\n🚀 Ready to track GPS data!")

if __name__ == "__main__":
    main()
