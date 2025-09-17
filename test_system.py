#!/usr/bin/env python3
"""
Test script for GPS Area Tracking System
"""

import requests
import json
from datetime import datetime, timedelta
import time

BASE_URL = "http://localhost:17890"

def test_health():
    """Test system health"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Health check: {response.status_code}")
        print(f"   Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_api_status():
    """Test API status"""
    try:
        response = requests.get(f"{BASE_URL}/api/status")
        print(f"✅ API status: {response.status_code}")
        print(f"   Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ API status failed: {e}")
        return False

def create_test_vehicle():
    """Create a test vehicle"""
    vehicle_data = {
        "vehicle_id": "TEST001",
        "license_plate": "ทดสอบ-001",
        "vehicle_type": "truck",
        "driver_name": "ทดสอบ ระบบ",
        "driver_phone": "0812345678"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/vehicles/", json=vehicle_data)
        print(f"✅ Create vehicle: {response.status_code}")
        if response.status_code == 200:
            print(f"   Vehicle created: {response.json()}")
        else:
            print(f"   Response: {response.text}")
        return True
    except Exception as e:
        print(f"❌ Create vehicle failed: {e}")
        return False

def send_gps_data():
    """Send GPS data"""
    gps_data = {
        "vehicle_id": "TEST001",
        "latitude": 13.7563,
        "longitude": 100.5018,
        "speed": 45.5,
        "heading": 180.0,
        "accuracy": 5.0,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/gps/data", json=gps_data)
        print(f"✅ Send GPS data: {response.status_code}")
        if response.status_code == 200:
            print(f"   GPS data sent: {response.json()}")
        else:
            print(f"   Response: {response.text}")
        return True
    except Exception as e:
        print(f"❌ Send GPS data failed: {e}")
        return False

def create_test_area():
    """Create a test area"""
    area_data = {
        "name": "พื้นที่ทดสอบ",
        "area_type": "alert",
        "shape": "circle",
        "coordinates": {
            "center": {"lat": 13.7563, "lng": 100.5018},
            "radius": 0.01
        },
        "buffer_distance": 50.0
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/areas/", json=area_data)
        print(f"✅ Create area: {response.status_code}")
        if response.status_code == 200:
            print(f"   Area created: {response.json()}")
        else:
            print(f"   Response: {response.text}")
        return True
    except Exception as e:
        print(f"❌ Create area failed: {e}")
        return False

def get_dashboard_stats():
    """Get dashboard statistics"""
    try:
        response = requests.get(f"{BASE_URL}/api/dashboard/stats")
        print(f"✅ Dashboard stats: {response.status_code}")
        if response.status_code == 200:
            stats = response.json()
            print(f"   Total vehicles: {stats.get('total_vehicles', 0)}")
            print(f"   Active vehicles: {stats.get('active_vehicles', 0)}")
            print(f"   Average speed: {stats.get('average_speed', 0):.2f} km/h")
        else:
            print(f"   Response: {response.text}")
        return True
    except Exception as e:
        print(f"❌ Dashboard stats failed: {e}")
        return False

def get_vehicle_locations():
    """Get vehicle locations"""
    try:
        response = requests.get(f"{BASE_URL}/api/dashboard/vehicle-locations")
        print(f"✅ Vehicle locations: {response.status_code}")
        if response.status_code == 200:
            locations = response.json()
            print(f"   Found {len(locations)} vehicle locations")
            for loc in locations[:3]:  # Show first 3
                print(f"   - {loc['vehicle_id']}: {loc['latitude']:.6f}, {loc['longitude']:.6f}")
        else:
            print(f"   Response: {response.text}")
        return True
    except Exception as e:
        print(f"❌ Vehicle locations failed: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 60)
    print("🧪 GPS Area Tracking System - Test Suite")
    print("=" * 60)
    
    # Wait for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(2)
    
    # Test basic connectivity
    print("\n📡 Testing basic connectivity...")
    if not test_health():
        print("❌ Server is not running. Please start the server first:")
        print("   python run.py")
        return
    
    test_api_status()
    
    # Test vehicle management
    print("\n🚗 Testing vehicle management...")
    create_test_vehicle()
    
    # Test GPS data
    print("\n📍 Testing GPS data...")
    send_gps_data()
    
    # Test area management
    print("\n🗺️  Testing area management...")
    create_test_area()
    
    # Test dashboard
    print("\n📊 Testing dashboard...")
    get_dashboard_stats()
    get_vehicle_locations()
    
    print("\n" + "=" * 60)
    print("🎉 Test completed!")
    print("=" * 60)
    print("\n🌐 Open your browser and go to:")
    print(f"   {BASE_URL}")
    print("\n📚 API Documentation:")
    print(f"   {BASE_URL}/docs")

if __name__ == "__main__":
    main()
