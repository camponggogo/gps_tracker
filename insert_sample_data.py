#!/usr/bin/env python3
"""
Insert Sample Data for GPS Area Tracking System
"""

import mysql.connector
from datetime import datetime, timedelta
import random
import json

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '123456!',
    'database': 'gps_track_db',
    'charset': 'utf8mb4'
}

def connect_database():
    """Connect to MariaDB/MySQL database"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as e:
        print(f"❌ Database connection failed: {e}")
        return None

def insert_sample_vehicles(cursor):
    """Insert sample vehicles"""
    print("🚗 Inserting sample vehicles...")
    
    vehicles = [
        ("VH001", "ABC-1234", "truck", "active", "Driver A", "081-234-5678"),
        ("VH002", "DEF-5678", "truck", "active", "Driver B", "082-345-6789"),
        ("VH003", "GHI-9012", "truck", "active", "Driver C", "083-456-7890"),
        ("VH004", "JKL-3456", "truck", "active", "Driver D", "084-567-8901"),
        ("VH005", "MNO-7890", "truck", "active", "Driver E", "085-678-9012"),
        ("VH006", "PQR-1234", "van", "active", "Driver F", "086-789-0123"),
        ("VH007", "STU-5678", "van", "active", "Driver G", "087-890-1234"),
        ("VH008", "VWX-9012", "truck", "active", "Driver H", "088-901-2345"),
        ("VH009", "YZA-3456", "truck", "active", "Driver I", "089-012-3456"),
        ("VH010", "BCD-7890", "truck", "active", "Driver J", "090-123-4567")
    ]
    
    cursor.executemany("""
        INSERT IGNORE INTO vehicles (vehicle_id, license_plate, vehicle_type, status, driver_name, driver_phone) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """, vehicles)
    print(f"✅ Inserted {len(vehicles)} vehicles")

def insert_sample_areas(cursor):
    """Insert sample areas"""
    print("📍 Inserting sample areas...")
    
    # Bangkok coordinates
    areas = [
        ("Entrance Gate", "entrance", "polygon", json.dumps([
            [13.7563, 100.5018],
            [13.7573, 100.5028],
            [13.7563, 100.5038],
            [13.7553, 100.5028]
        ]), 50.0),
        ("Alert Zone 1", "alert", "circle", json.dumps({
            "center": [13.7663, 100.5118],
            "radius": 100
        }), 0.0),
        ("Critical Zone", "critical", "rectangle", json.dumps({
            "north": 13.7763,
            "south": 13.7563,
            "east": 100.5218,
            "west": 100.5018
        }), 0.0),
        ("Checkpoint Warehouse", "checkpoint", "polygon", json.dumps([
            [13.7463, 100.4918],
            [13.7473, 100.4928],
            [13.7463, 100.4938],
            [13.7453, 100.4928]
        ]), 30.0),
        ("Speed Alert Zone", "alert", "circle", json.dumps({
            "center": [13.7363, 100.4818],
            "radius": 200
        }), 0.0)
    ]
    
    cursor.executemany("""
        INSERT IGNORE INTO areas (name, area_type, shape, coordinates, buffer_distance) 
        VALUES (%s, %s, %s, %s, %s)
    """, areas)
    print(f"✅ Inserted {len(areas)} areas")

def insert_sample_gps_logs(cursor):
    """Insert sample GPS logs"""
    print("📍 Inserting sample GPS logs...")
    
    # Get vehicle IDs
    cursor.execute("SELECT id FROM vehicles ORDER BY id")
    vehicle_ids = [row[0] for row in cursor.fetchall()]
    
    if not vehicle_ids:
        print("❌ No vehicles found. Please insert vehicles first.")
        return
    
    # Generate GPS logs for each vehicle
    gps_logs = []
    base_time = datetime.now() - timedelta(hours=2)
    
    for i, vehicle_id in enumerate(vehicle_ids):
        # Generate 20 GPS points for each vehicle
        for j in range(20):
            # Create a route pattern
            lat_offset = random.uniform(-0.01, 0.01)
            lon_offset = random.uniform(-0.01, 0.01)
            
            latitude = 13.7563 + lat_offset + (j * 0.001)
            longitude = 100.5018 + lon_offset + (j * 0.001)
            speed = random.uniform(20, 80)
            heading = random.uniform(0, 360)
            accuracy = random.uniform(3, 8)
            
            timestamp = base_time + timedelta(minutes=j*3 + i*5)
            
            gps_logs.append((
                vehicle_id, latitude, longitude, speed, heading, accuracy, timestamp
            ))
    
    cursor.executemany("""
        INSERT IGNORE INTO gps_logs (vehicle_id, latitude, longitude, speed, heading, accuracy, timestamp) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, gps_logs)
    print(f"✅ Inserted {len(gps_logs)} GPS logs")

def insert_sample_routes(cursor):
    """Insert sample routes"""
    print("🛣️ Inserting sample routes...")
    
    # Get vehicle IDs
    cursor.execute("SELECT id FROM vehicles ORDER BY id")
    vehicle_ids = [row[0] for row in cursor.fetchall()]
    
    routes = []
    base_time = datetime.now() - timedelta(hours=1)
    
    for i, vehicle_id in enumerate(vehicle_ids):
        start_time = base_time + timedelta(minutes=i*10)
        end_time = start_time + timedelta(minutes=random.randint(30, 120))
        
        # Random start and end points
        start_lat = 13.7563 + random.uniform(-0.01, 0.01)
        start_lon = 100.5018 + random.uniform(-0.01, 0.01)
        end_lat = 13.7663 + random.uniform(-0.01, 0.01)
        end_lon = 100.5118 + random.uniform(-0.01, 0.01)
        
        # Calculate distance (simplified)
        distance = random.uniform(5, 50)
        duration = int((end_time - start_time).total_seconds() / 60)
        
        routes.append((
            vehicle_id, start_lat, start_lon, end_lat, end_lon,
            start_time, end_time, distance, duration
        ))
    
    cursor.executemany("""
        INSERT IGNORE INTO routes (vehicle_id, start_latitude, start_longitude, end_latitude, end_longitude, 
                                 start_time, end_time, total_distance, total_duration) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, routes)
    print(f"✅ Inserted {len(routes)} routes")

def insert_sample_alerts(cursor):
    """Insert sample alerts"""
    print("🚨 Inserting sample alerts...")
    
    # Get vehicle and area IDs
    cursor.execute("SELECT id FROM vehicles ORDER BY id LIMIT 5")
    vehicle_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT id FROM areas WHERE area_type = 'alert' OR area_type = 'critical'")
    area_ids = [row[0] for row in cursor.fetchall()]
    
    alerts = []
    base_time = datetime.now() - timedelta(hours=1)
    
    for i, vehicle_id in enumerate(vehicle_ids):
        for j in range(3):  # 3 alerts per vehicle
            alert_time = base_time + timedelta(minutes=j*20 + i*10)
            area_id = area_ids[j % len(area_ids)] if area_ids else None
            
            alert_types = ["speed_exceeded", "area_entry", "idle_timeout"]
            messages = [
                "Vehicle exceeded speed limit",
                "Vehicle entered restricted area",
                "Vehicle idle for too long"
            ]
            
            alert_type = alert_types[j % len(alert_types)]
            message = messages[j % len(messages)]
            
            latitude = 13.7563 + random.uniform(-0.01, 0.01)
            longitude = 100.5018 + random.uniform(-0.01, 0.01)
            
            alerts.append((
                vehicle_id, area_id, alert_type, message, latitude, longitude, False, alert_time
            ))
    
    cursor.executemany("""
        INSERT IGNORE INTO alerts (vehicle_id, area_id, alert_type, message, latitude, longitude, is_resolved, created_at) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, alerts)
    print(f"✅ Inserted {len(alerts)} alerts")

def insert_sample_dashboard_stats(cursor):
    """Insert sample dashboard statistics"""
    print("📊 Inserting sample dashboard statistics...")
    
    stats = [
        ("total_vehicles", 10, "Total Vehicles"),
        ("active_vehicles", 8, "Active Vehicles"),
        ("average_speed", 45.5, "Average Speed (km/h)"),
        ("total_distance", 1250.75, "Total Distance (km)"),
        ("alerts_today", 15, "Alerts Today"),
        ("vehicles_in_warehouse", 3, "Vehicles in Warehouse"),
        ("completed_deliveries", 12, "Completed Deliveries"),
        ("fuel_efficiency", 8.5, "Fuel Efficiency (km/l)")
    ]
    
    cursor.executemany("""
        INSERT IGNORE INTO dashboard_stats (stat_type, stat_value, stat_label, timestamp) 
        VALUES (%s, %s, %s, %s)
    """, [(stat_type, stat_value, stat_label, datetime.now()) for stat_type, stat_value, stat_label in stats])
    print(f"✅ Inserted {len(stats)} dashboard statistics")

def main():
    """Main function to insert sample data"""
    print("=" * 60)
    print("📊 Insert Sample Data for GPS Area Tracking System")
    print("=" * 60)
    
    # Connect to database
    connection = connect_database()
    if not connection:
        return
    
    try:
        cursor = connection.cursor()
        
        # Insert sample data
        insert_sample_vehicles(cursor)
        insert_sample_areas(cursor)
        insert_sample_gps_logs(cursor)
        insert_sample_routes(cursor)
        insert_sample_alerts(cursor)
        insert_sample_dashboard_stats(cursor)
        
        # Commit changes
        connection.commit()
        
        print("\n" + "=" * 60)
        print("🎉 Sample data insertion completed successfully!")
        print("=" * 60)
        
        # Show summary
        cursor.execute("SELECT COUNT(*) FROM vehicles")
        vehicle_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM gps_logs")
        gps_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM areas")
        area_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM alerts")
        alert_count = cursor.fetchone()[0]
        
        print(f"📋 Data Summary:")
        print(f"   🚗 Vehicles: {vehicle_count}")
        print(f"   📍 GPS Logs: {gps_count}")
        print(f"   🗺️  Areas: {area_count}")
        print(f"   🚨 Alerts: {alert_count}")
        
    except mysql.connector.Error as e:
        print(f"❌ Error inserting sample data: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    main()
