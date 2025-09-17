#!/bin/bash

echo "============================================================"
echo "🗄️  MariaDB Installation for Ubuntu/Debian"
echo "============================================================"
echo

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "⚠️  Running as root. This is not recommended for security reasons."
    echo "Please run this script as a regular user with sudo privileges."
    exit 1
fi

# Check if MariaDB is already installed
if command -v mysql &> /dev/null; then
    echo "✅ MariaDB/MySQL is already installed"
    mysql --version
    echo
    read -p "Do you want to continue with setup? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Installation cancelled"
        exit 0
    fi
fi

echo "🔧 Updating package list..."
sudo apt update

echo "📦 Installing MariaDB server..."
sudo apt install -y mariadb-server mariadb-client

if [ $? -ne 0 ]; then
    echo "❌ Failed to install MariaDB"
    exit 1
fi

echo "✅ MariaDB installed successfully"

echo "🔧 Starting MariaDB service..."
sudo systemctl start mariadb
sudo systemctl enable mariadb

echo "🔒 Securing MariaDB installation..."
echo "You will be prompted to set a root password and configure security options."
echo "Press Enter to continue..."
read

sudo mysql_secure_installation

echo "🔧 Creating database and user for GPS tracking system..."
echo "Please enter the following information:"
echo

read -p "Enter MariaDB root password: " -s ROOT_PASSWORD
echo

read -p "Enter database name (default: gps_track_db): " DB_NAME
DB_NAME=${DB_NAME:-gps_track_db}

read -p "Enter database user (default: gps_user): " DB_USER
DB_USER=${DB_USER:-gps_user}

read -p "Enter database password: " -s DB_PASSWORD
echo

echo "📝 Creating database and user..."

# Create SQL commands
SQL_COMMANDS="
CREATE DATABASE IF NOT EXISTS ${DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS '${DB_USER}'@'localhost' IDENTIFIED BY '${DB_PASSWORD}';
GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '${DB_USER}'@'localhost';
FLUSH PRIVILEGES;
"

# Execute SQL commands
echo "$SQL_COMMANDS" | sudo mysql -u root -p"$ROOT_PASSWORD"

if [ $? -ne 0 ]; then
    echo "❌ Failed to create database and user"
    echo "Please run the following commands manually:"
    echo "sudo mysql -u root -p"
    echo "CREATE DATABASE IF NOT EXISTS ${DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    echo "CREATE USER IF NOT EXISTS '${DB_USER}'@'localhost' IDENTIFIED BY '${DB_PASSWORD}';"
    echo "GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '${DB_USER}'@'localhost';"
    echo "FLUSH PRIVILEGES;"
    echo "EXIT;"
    exit 1
fi

echo "✅ Database and user created successfully"

echo "📝 Creating .env file with database configuration..."
cat > .env << EOF
# Database Configuration
DATABASE_URL=mysql+pymysql://${DB_USER}:${DB_PASSWORD}@localhost:3306/${DB_NAME}
DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_NAME=${DB_NAME}
DATABASE_USER=${DB_USER}
DATABASE_PASSWORD=${DB_PASSWORD}

# API Configuration
API_HOST=0.0.0.0
API_PORT=17890
API_DEBUG=true

# Security Configuration
SECRET_KEY=_5wwvZWMjUUpK7eg5sklHh8mpQE0UNtQSVabpIE0ArY
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# GPS Configuration
GPS_UPDATE_INTERVAL=30

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/gps_tracking.log
EOF

echo "✅ .env file created"

echo "🔧 Testing database connection..."
python3 -c "
import mysql.connector
try:
    conn = mysql.connector.connect(
        host='localhost',
        user='${DB_USER}',
        password='${DB_PASSWORD}',
        database='${DB_NAME}'
    )
    print('✅ Database connection successful')
    conn.close()
except Exception as e:
    print(f'❌ Database connection failed: {e}')
    exit(1)
"

if [ $? -ne 0 ]; then
    echo "❌ Database connection test failed"
    exit 1
fi

echo
echo "============================================================"
echo "🎉 MariaDB installation and setup completed successfully!"
echo "============================================================"
echo
echo "📋 Database Information:"
echo "   Host: localhost"
echo "   Port: 3306"
echo "   Database: ${DB_NAME}"
echo "   User: ${DB_USER}"
echo "   Password: [HIDDEN]"
echo
echo "📋 Next steps:"
echo "1. Run: ./setup_venv.sh"
echo "2. Run: python setup_mariadb.py"
echo "3. Run: python insert_sample_data.py"
echo "4. Run: ./run_with_venv.sh"
echo
echo "🌐 Access URLs:"
echo "   http://localhost:17890           - Main interface"
echo "   http://localhost:17890/docs     - API documentation"
echo
echo "🚀 Ready to run the GPS tracking system!"
echo
