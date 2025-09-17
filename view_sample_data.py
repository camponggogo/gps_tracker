#!/usr/bin/env python3
"""
View Sample Data in GPS Area Tracking System Database
"""

import mysql.connector
from datetime import datetime

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

def view_vehicles(cursor):
    """View vehicles data"""
    print("🚗 Vehicles:")
    print("-" * 80)
    cursor.execute("""
        SELECT vehicle_id, license_plate, vehicle_type, status, driver_name, driver_phone, created_at
        FROM vehicles 
        ORDER BY vehicle_id
    """)
    
    vehicles = cursor.fetchall()
    print(f"{'ID':<8} {'License':<12} {'Type':<10} {'Status':<12} {'Driver':<15} {'Phone':<15} {'Created'}")
    print("-" * 80)
    
    for vehicle in vehicles:
        vehicle_id, license_plate, vehicle_type, status, driver_name, driver_phone, created_at = vehicle
        print(f"{vehicle_id:<8} {license_plate:<12} {vehicle_type:<10} {status:<12} {driver_name:<15} {driver_phone:<15} {created_at}")
    
    print(f"\nTotal vehicles: {len(vehicles)}")
    print()

def view_areas(cursor):
    """View areas data"""
    print("📍 Areas:")
    print("-" * 100)
    cursor.execute("""
        SELECT name, area_type, shape, buffer_distance, is_active, created_at
        FROM areas 
        ORDER BY area_type, name
    """)
    
    areas = cursor.fetchall()
    print(f"{'Name':<20} {'Type':<12} {'Shape':<10} {'Buffer':<8} {'Active':<8} {'Created'}")
    print("-" * 100)
    
    for area in areas:
        name, area_type, shape, buffer_distance, is_active, created_at = area
        print(f"{name:<20} {area_type:<12} {shape:<10} {buffer_distance:<8} {'Yes' if is_active else 'No':<8} {created_at}")
    
    print(f"\nTotal areas: {len(areas)}")
    print()

def view_gps_logs_summary(cursor):
    """View GPS logs summary"""
    print("📍 GPS Logs Summary:")
    print("-" * 60)
    
    # Total GPS logs
    cursor.execute("SELECT COUNT(*) FROM gps_logs")
    total_logs = cursor.fetchone()[0]
    
    # Latest GPS logs per vehicle
    cursor.execute("""
        SELECT v.vehicle_id, v.license_plate, gl.latitude, gl.longitude, gl.speed, gl.timestamp
        FROM vehicles v
        JOIN gps_logs gl ON v.id = gl.vehicle_id
        WHERE gl.timestamp = (
            SELECT MAX(timestamp) 
            FROM gps_logs gl2 
            WHERE gl2.vehicle_id = gl.vehicle_id
        )
        ORDER BY v.vehicle_id
    """)
    
    latest_logs = cursor.fetchall()
    print(f"{'Vehicle':<8} {'License':<12} {'Latitude':<12} {'Longitude':<12} {'Speed':<8} {'Last Update'}")
    print("-" * 60)
    
    for log in latest_logs:
        vehicle_id, license_plate, latitude, longitude, speed, timestamp = log
        print(f"{vehicle_id:<8} {license_plate:<12} {latitude:<12.6f} {longitude:<12.6f} {speed:<8.1f} {timestamp}")
    
    print(f"\nTotal GPS logs: {total_logs}")
    print(f"Latest positions for {len(latest_logs)} vehicles")
    print()

def view_routes(cursor):
    """View routes data"""
    print("🛣️ Routes:")
    print("-" * 100)
    cursor.execute("""
        SELECT v.vehicle_id, v.license_plate, r.start_latitude, r.start_longitude, 
               r.end_latitude, r.end_longitude, r.total_distance, r.total_duration, r.start_time, r.end_time
        FROM routes r
        JOIN vehicles v ON r.vehicle_id = v.id
        ORDER BY r.start_time DESC
        LIMIT 10
    """)
    
    routes = cursor.fetchall()
    print(f"{'Vehicle':<8} {'License':<12} {'Start':<20} {'End':<20} {'Distance':<10} {'Duration':<10} {'Start Time'}")
    print("-" * 100)
    
    for route in routes:
        vehicle_id, license_plate, start_lat, start_lon, end_lat, end_lon, distance, duration, start_time, end_time = route
        start_coord = f"{start_lat:.4f},{start_lon:.4f}"
        end_coord = f"{end_lat:.4f},{end_lon:.4f}"
        print(f"{vehicle_id:<8} {license_plate:<12} {start_coord:<20} {end_coord:<20} {distance:<10.2f} {duration:<10} {start_time}")
    
    print(f"\nShowing latest {len(routes)} routes")
    print()

def view_alerts(cursor):
    """View alerts data"""
    print("🚨 Alerts:")
    print("-" * 100)
    cursor.execute("""
        SELECT v.vehicle_id, v.license_plate, a.alert_type, a.message, a.is_resolved, a.created_at
        FROM alerts a
        JOIN vehicles v ON a.vehicle_id = v.id
        ORDER BY a.created_at DESC
        LIMIT 15
    """)
    
    alerts = cursor.fetchall()
    print(f"{'Vehicle':<8} {'License':<12} {'Type':<15} {'Message':<25} {'Resolved':<10} {'Created'}")
    print("-" * 100)
    
    for alert in alerts:
        vehicle_id, license_plate, alert_type, message, is_resolved, created_at = alert
        resolved_text = "Yes" if is_resolved else "No"
        print(f"{vehicle_id:<8} {license_plate:<12} {alert_type:<15} {message[:25]:<25} {resolved_text:<10} {created_at}")
    
    print(f"\nShowing latest {len(alerts)} alerts")
    print()

def view_dashboard_stats(cursor):
    """View dashboard statistics"""
    print("📊 Dashboard Statistics:")
    print("-" * 50)
    cursor.execute("""
        SELECT stat_type, stat_value, stat_label, timestamp
        FROM dashboard_stats 
        ORDER BY stat_type
    """)
    
    stats = cursor.fetchall()
    print(f"{'Type':<20} {'Value':<15} {'Label':<25} {'Updated'}")
    print("-" * 50)
    
    for stat in stats:
        stat_type, stat_value, stat_label, timestamp = stat
        print(f"{stat_type:<20} {stat_value:<15} {stat_label:<25} {timestamp}")
    
    print(f"\nTotal statistics: {len(stats)}")
    print()

def main():
    """Main function to view sample data"""
    print("=" * 80)
    print("📊 GPS Area Tracking System - Database Viewer")
    print("=" * 80)
    
    # Connect to database
    connection = connect_database()
    if not connection:
        return
    
    try:
        cursor = connection.cursor()
        
        # View all data
        view_vehicles(cursor)
        view_areas(cursor)
        view_gps_logs_summary(cursor)
        view_routes(cursor)
        view_alerts(cursor)
        view_dashboard_stats(cursor)
        
        print("=" * 80)
        print("🎉 Database viewing completed!")
        print("=" * 80)
        
    except mysql.connector.Error as e:
        print(f"❌ Error viewing data: {e}")
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    main()
