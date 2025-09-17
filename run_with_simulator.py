#!/usr/bin/env python3
"""
Run GPS Area Tracking System with Vehicle Simulator
"""

import subprocess
import sys
import time
import threading
import os
from pathlib import Path

def run_server():
    """Run the GPS tracking server"""
    print("🚀 Starting GPS tracking server...")
    try:
        subprocess.run([sys.executable, "run.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Server error: {e}")
    except KeyboardInterrupt:
        print("👋 Server stopped")

def run_simulator():
    """Run the vehicle simulator"""
    print("🚗 Starting vehicle simulator...")
    simulator_dir = Path("simulator")
    if not simulator_dir.exists():
        print("❌ Simulator directory not found")
        return
    
    try:
        subprocess.run([sys.executable, "start_simulator.py"], 
                      cwd=simulator_dir, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Simulator error: {e}")
    except KeyboardInterrupt:
        print("👋 Simulator stopped")

def main():
    """Main function"""
    print("=" * 60)
    print("🚗 GPS Area Tracking System + Vehicle Simulator")
    print("=" * 60)
    print()
    print("📋 This will start:")
    print("   1. GPS tracking server on port 17890")
    print("   2. Vehicle simulator with 10 vehicles")
    print()
    print("🗺️  Open http://localhost:17890 to see the map")
    print("⏹️  Press Ctrl+C to stop everything")
    print("-" * 60)
    
    # Wait a moment for user to read
    time.sleep(3)
    
    try:
        # Start server in a separate thread
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        
        # Wait for server to start
        print("⏳ Waiting for server to start...")
        time.sleep(5)
        
        # Start simulator
        run_simulator()
        
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
