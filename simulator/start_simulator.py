#!/usr/bin/env python3
"""
Start GPS Vehicle Simulator
"""

import sys
import subprocess
import time
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import aiohttp
        print("✅ aiohttp is installed")
        return True
    except ImportError:
        print("❌ aiohttp is not installed")
        print("📦 Installing aiohttp...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "aiohttp"], check=True)
            print("✅ aiohttp installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install aiohttp")
            return False

def main():
    """Main function"""
    print("=" * 60)
    print("🚗 GPS Vehicle Simulator Launcher")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Cannot start simulator due to missing dependencies")
        return
    
    print("\n🚀 Starting vehicle simulator...")
    print("📍 Make sure the GPS tracking server is running on port 17890")
    print("🗺️  Open http://localhost:17890 to see the map")
    print("⏹️  Press Ctrl+C to stop")
    print("-" * 60)
    
    try:
        # Import and run the simulator
        from vehicle_simulator import main as run_simulator
        run_simulator()
    except KeyboardInterrupt:
        print("\n👋 Simulator stopped by user")
    except Exception as e:
        print(f"\n❌ Simulator error: {e}")

if __name__ == "__main__":
    main()
