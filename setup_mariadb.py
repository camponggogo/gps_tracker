#!/usr/bin/env python3
"""
MariaDB/MySQL Setup Script for GPS Area Tracking System
"""

import pymysql
import sys
from pathlib import Path

def connect_to_mariadb():
    """Connect to MariaDB/MySQL"""
    try:
        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='123456!',
            charset='utf8mb4'
        )
        print("✅ Connected to MariaDB/MySQL successfully")
        return connection
    except Exception as e:
        print(f"❌ Failed to connect to MariaDB/MySQL: {e}")
        return None

def create_database(connection):
    """Create database if not exists"""
    try:
        cursor = connection.cursor()
        
        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS gps_track_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print("✅ Database 'gps_track_db' created/verified")
        
        # Use the database
        cursor.execute("USE gps_track_db")
        print("✅ Using database 'gps_track_db'")
        
        cursor.close()
        return True
    except Exception as e:
        print(f"❌ Failed to create database: {e}")
        return False

def create_tables(connection):
    """Create all necessary tables"""
    try:
        cursor = connection.cursor()
        
        # Create vehicles table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vehicles (
                id INT AUTO_INCREMENT PRIMARY KEY,
                vehicle_id VARCHAR(50) UNIQUE NOT NULL,
                license_plate VARCHAR(20) UNIQUE,
                vehicle_type ENUM('truck', 'van', 'motorcycle', 'car', 'bus') NOT NULL,
                status ENUM('active', 'inactive', 'maintenance', 'breakdown') DEFAULT 'active',
                driver_name VARCHAR(100),
                driver_phone VARCHAR(20),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_vehicle_id (vehicle_id),
                INDEX idx_license_plate (license_plate),
                INDEX idx_status (status),
                INDEX idx_vehicle_type (vehicle_type)
            )
        """)
        print("✅ Created vehicles table")
        
        # Create gps_logs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS gps_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                vehicle_id INT NOT NULL,
                latitude DECIMAL(10, 8) NOT NULL,
                longitude DECIMAL(11, 8) NOT NULL,
                altitude DECIMAL(8, 2),
                speed DECIMAL(6, 2),
                heading DECIMAL(6, 2),
                accuracy DECIMAL(8, 2),
                timestamp TIMESTAMP NOT NULL,
                is_idle BOOLEAN DEFAULT FALSE,
                idle_duration INT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE,
                INDEX idx_vehicle_id (vehicle_id),
                INDEX idx_timestamp (timestamp),
                INDEX idx_location (latitude, longitude),
                INDEX idx_is_idle (is_idle)
            )
        """)
        print("✅ Created gps_logs table")
        
        # Create areas table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS areas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                area_type ENUM('entrance', 'alert', 'critical', 'checkpoint') NOT NULL,
                shape ENUM('polygon', 'circle', 'rectangle') NOT NULL,
                coordinates JSON NOT NULL,
                buffer_distance DECIMAL(8, 2) DEFAULT 0.0,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_area_type (area_type),
                INDEX idx_shape (shape),
                INDEX idx_is_active (is_active)
            )
        """)
        print("✅ Created areas table")
        
        # Create alerts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                vehicle_id INT NOT NULL,
                area_id INT,
                alert_type VARCHAR(50) NOT NULL,
                message TEXT NOT NULL,
                latitude DECIMAL(10, 8),
                longitude DECIMAL(11, 8),
                is_resolved BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                resolved_at TIMESTAMP NULL,
                FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE,
                FOREIGN KEY (area_id) REFERENCES areas(id) ON DELETE SET NULL,
                INDEX idx_vehicle_id (vehicle_id),
                INDEX idx_area_id (area_id),
                INDEX idx_alert_type (alert_type),
                INDEX idx_is_resolved (is_resolved),
                INDEX idx_created_at (created_at)
            )
        """)
        print("✅ Created alerts table")
        
        # Create routes table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS routes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                vehicle_id INT NOT NULL,
                start_latitude DECIMAL(10, 8) NOT NULL,
                start_longitude DECIMAL(11, 8) NOT NULL,
                end_latitude DECIMAL(10, 8) NOT NULL,
                end_longitude DECIMAL(11, 8) NOT NULL,
                start_time TIMESTAMP NOT NULL,
                end_time TIMESTAMP NULL,
                total_distance DECIMAL(10, 2),
                total_duration INT,
                average_speed DECIMAL(6, 2),
                max_speed DECIMAL(6, 2),
                idle_time INT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE,
                INDEX idx_vehicle_id (vehicle_id),
                INDEX idx_start_time (start_time),
                INDEX idx_end_time (end_time)
            )
        """)
        print("✅ Created routes table")
        
        # Create dashboard_stats table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dashboard_stats (
                id INT AUTO_INCREMENT PRIMARY KEY,
                stat_type VARCHAR(50) NOT NULL,
                stat_value DECIMAL(15, 2) NOT NULL,
                stat_label VARCHAR(100),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata JSON,
                INDEX idx_stat_type (stat_type),
                INDEX idx_timestamp (timestamp)
            )
        """)
        print("✅ Created dashboard_stats table")
        
        cursor.close()
        return True
    except Exception as e:
        print(f"❌ Failed to create tables: {e}")
        return False

def insert_sample_data(connection):
    """Insert sample data"""
    try:
        cursor = connection.cursor()
        
        # Insert sample vehicles
        vehicles_data = [
            ('V001', 'กข-1234', 'truck', 'สมชาย ใจดี', '0812345678'),
            ('V002', 'กข-5678', 'van', 'สมหญิง รักดี', '0823456789'),
            ('V003', 'กข-9012', 'motorcycle', 'สมศักดิ์ เก่งดี', '0834567890'),
            ('V004', 'กข-3456', 'car', 'สมพร สวยดี', '0845678901'),
            ('V005', 'กข-7890', 'bus', 'สมบัติ ดีดี', '0856789012')
        ]
        
        cursor.executemany("""
            INSERT IGNORE INTO vehicles (vehicle_id, license_plate, vehicle_type, driver_name, driver_phone) 
            VALUES (%s, %s, %s, %s, %s)
        """, vehicles_data)
        print("✅ Inserted sample vehicles")
        
        # Insert sample areas
        areas_data = [
            ('คลังสินค้าหลัก', 'checkpoint', 'rectangle', '{"bounds": {"north": 13.8, "south": 13.7, "east": 100.6, "west": 100.5}}', 50.0),
            ('พื้นที่แจ้งเตือน', 'alert', 'circle', '{"center": {"lat": 13.7563, "lng": 100.5018}, "radius": 0.01}', 100.0),
            ('พื้นที่วิกฤต', 'critical', 'polygon', '{"points": [{"lat": 13.75, "lng": 100.50}, {"lat": 13.76, "lng": 100.50}, {"lat": 13.76, "lng": 100.51}, {"lat": 13.75, "lng": 100.51}]}', 25.0),
            ('ทางเข้าหลัก', 'entrance', 'rectangle', '{"bounds": {"north": 13.77, "south": 13.74, "east": 100.52, "west": 100.49}}', 30.0)
        ]
        
        cursor.executemany("""
            INSERT IGNORE INTO areas (name, area_type, shape, coordinates, buffer_distance) 
            VALUES (%s, %s, %s, %s, %s)
        """, areas_data)
        print("✅ Inserted sample areas")
        
        # Insert sample GPS logs (using vehicle IDs from vehicles table)
        cursor.execute("SELECT id FROM vehicles ORDER BY id")
        vehicle_ids = [row[0] for row in cursor.fetchall()]
        
        gps_data = [
            (vehicle_ids[0], 13.7563, 100.5018, 45.5, 180.0, 5.0),
            (vehicle_ids[1], 13.7663, 100.5118, 35.2, 90.0, 3.0),
            (vehicle_ids[2], 13.7463, 100.4918, 60.0, 270.0, 8.0),
            (vehicle_ids[3], 13.7763, 100.5218, 25.0, 0.0, 4.0),
            (vehicle_ids[4], 13.7363, 100.4818, 55.5, 135.0, 6.0)
        ]
        
        cursor.executemany("""
            INSERT IGNORE INTO gps_logs (vehicle_id, latitude, longitude, speed, heading, accuracy, timestamp) 
            VALUES (%s, %s, %s, %s, %s, %s, NOW())
        """, gps_data)
        print("✅ Inserted sample GPS logs")
        
        connection.commit()
        cursor.close()
        return True
    except Exception as e:
        print(f"❌ Failed to insert sample data: {e}")
        return False

def create_views(connection):
    """Create useful views"""
    try:
        cursor = connection.cursor()
        
        # Create vehicle_latest_locations view
        cursor.execute("""
            CREATE OR REPLACE VIEW vehicle_latest_locations AS
            SELECT 
                v.id,
                v.vehicle_id,
                v.license_plate,
                v.vehicle_type,
                v.status,
                v.driver_name,
                gl.latitude,
                gl.longitude,
                gl.speed,
                gl.heading,
                gl.timestamp,
                gl.is_idle
            FROM vehicles v
            LEFT JOIN gps_logs gl ON v.id = gl.vehicle_id
            WHERE gl.timestamp = (
                SELECT MAX(timestamp) 
                FROM gps_logs gl2 
                WHERE gl2.vehicle_id = v.id
            )
        """)
        print("✅ Created vehicle_latest_locations view")
        
        # Create dashboard_summary view
        cursor.execute("""
            CREATE OR REPLACE VIEW dashboard_summary AS
            SELECT 
                COUNT(DISTINCT v.id) as total_vehicles,
                COUNT(DISTINCT CASE WHEN v.status = 'active' THEN v.id END) as active_vehicles,
                COUNT(DISTINCT CASE WHEN v.status = 'inactive' THEN v.id END) as inactive_vehicles,
                COUNT(DISTINCT CASE WHEN v.status = 'maintenance' THEN v.id END) as maintenance_vehicles,
                COUNT(DISTINCT CASE WHEN v.status = 'breakdown' THEN v.id END) as breakdown_vehicles,
                AVG(CASE WHEN gl.speed > 0 THEN gl.speed END) as average_speed,
                COUNT(DISTINCT CASE WHEN gl.is_idle = TRUE THEN v.id END) as idle_vehicles
            FROM vehicles v
            LEFT JOIN gps_logs gl ON v.id = gl.vehicle_id
            WHERE gl.timestamp >= DATE_SUB(NOW(), INTERVAL 1 HOUR)
        """)
        print("✅ Created dashboard_summary view")
        
        cursor.close()
        return True
    except Exception as e:
        print(f"❌ Failed to create views: {e}")
        return False

def main():
    """Main setup function"""
    print("=" * 60)
    print("🗄️  MariaDB/MySQL Setup for GPS Area Tracking System")
    print("=" * 60)
    
    # Connect to MariaDB/MySQL
    connection = connect_to_mariadb()
    if not connection:
        sys.exit(1)
    
    try:
        # Create database
        if not create_database(connection):
            sys.exit(1)
        
        # Use the database
        cursor = connection.cursor()
        cursor.execute("USE gps_track_db")
        cursor.close()
        
        # Create tables
        if not create_tables(connection):
            sys.exit(1)
        
        # Insert sample data (optional)
        print("📝 Skipping sample data insertion for now...")
        # if not insert_sample_data(connection):
        #     sys.exit(1)
        
        # Create views (optional)
        print("📝 Skipping views creation for now...")
        # if not create_views(connection):
        #     sys.exit(1)
        
        print("\n" + "=" * 60)
        print("🎉 MariaDB/MySQL setup completed successfully!")
        print("=" * 60)
        print("\n📋 Database Information:")
        print("   Host: localhost")
        print("   Port: 3306")
        print("   Database: gps_track_db")
        print("   User: root")
        print("   Password: 123456!")
        print("\n🚀 Ready to run the GPS tracking system!")
        
    finally:
        connection.close()

if __name__ == "__main__":
    main()
