#!/usr/bin/env python3
"""
Clear Sample Data from GPS Area Tracking System Database
"""

import mysql.connector

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

def clear_all_data(cursor):
    """Clear all sample data from tables"""
    print("🗑️ Clearing all sample data...")
    
    # Clear data in reverse order of dependencies
    tables = [
        'dashboard_stats',
        'alerts', 
        'routes',
        'gps_logs',
        'areas',
        'vehicles'
    ]
    
    for table in tables:
        try:
            cursor.execute(f"DELETE FROM {table}")
            affected_rows = cursor.rowcount
            print(f"✅ Cleared {affected_rows} records from {table}")
        except mysql.connector.Error as e:
            print(f"❌ Error clearing {table}: {e}")

def reset_auto_increment(cursor):
    """Reset auto increment counters"""
    print("\n🔄 Resetting auto increment counters...")
    
    tables = [
        'vehicles',
        'gps_logs', 
        'areas',
        'alerts',
        'routes',
        'dashboard_stats'
    ]
    
    for table in tables:
        try:
            cursor.execute(f"ALTER TABLE {table} AUTO_INCREMENT = 1")
            print(f"✅ Reset auto increment for {table}")
        except mysql.connector.Error as e:
            print(f"❌ Error resetting {table}: {e}")

def show_table_counts(cursor):
    """Show current table counts"""
    print("\n📊 Current table counts:")
    print("-" * 40)
    
    tables = [
        'vehicles',
        'gps_logs', 
        'areas',
        'alerts',
        'routes',
        'dashboard_stats'
    ]
    
    for table in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"{table:<20}: {count}")
        except mysql.connector.Error as e:
            print(f"{table:<20}: Error - {e}")

def main():
    """Main function to clear sample data"""
    print("=" * 60)
    print("🗑️ Clear Sample Data from GPS Area Tracking System")
    print("=" * 60)
    
    # Connect to database
    connection = connect_database()
    if not connection:
        return
    
    try:
        cursor = connection.cursor()
        
        # Show current counts
        show_table_counts(cursor)
        
        # Ask for confirmation
        print("\n⚠️  WARNING: This will delete ALL sample data!")
        confirm = input("Are you sure you want to continue? (yes/no): ").lower().strip()
        
        if confirm in ['yes', 'y']:
            # Clear all data
            clear_all_data(cursor)
            
            # Reset auto increment
            reset_auto_increment(cursor)
            
            # Commit changes
            connection.commit()
            
            print("\n" + "=" * 60)
            print("🎉 Sample data cleared successfully!")
            print("=" * 60)
            
            # Show final counts
            show_table_counts(cursor)
            
        else:
            print("❌ Operation cancelled.")
            
    except mysql.connector.Error as e:
        print(f"❌ Error clearing data: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    main()
