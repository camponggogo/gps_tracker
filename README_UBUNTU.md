# 🐧 GPS Area Tracking System - Ubuntu Installation Guide

## 📋 System Requirements

- **Ubuntu 18.04+** หรือ **Debian 10+**
- **Python 3.8+**
- **MariaDB 10.3+**
- **RAM**: อย่างน้อย 2GB
- **Disk Space**: อย่างน้อย 1GB

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/camponggogo/gps_tracker.git
cd gps_tracker
```

### 2. Install Dependencies
```bash
chmod +x *.sh
./install_dependencies_ubuntu.sh
```

### 3. Install MariaDB
```bash
./install_mariadb_ubuntu.sh
```

### 4. Setup Database
```bash
source venv/bin/activate
python setup_mariadb.py
```

### 5. Insert Sample Data
```bash
python insert_sample_data.py
```

### 6. Run System
```bash
./run_with_venv.sh
```

## 📦 Manual Installation

### Install System Dependencies
```bash
sudo apt update
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    build-essential \
    libssl-dev \
    libffi-dev \
    libmysqlclient-dev \
    pkg-config \
    curl \
    git
```

### Install MariaDB
```bash
sudo apt install -y mariadb-server mariadb-client
sudo systemctl start mariadb
sudo systemctl enable mariadb
sudo mysql_secure_installation
```

### Create Database and User
```bash
sudo mysql -u root -p
```

```sql
CREATE DATABASE IF NOT EXISTS gps_track_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'gps_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON gps_track_db.* TO 'gps_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Setup Python Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Configure Environment
```bash
cp env.example .env
nano .env
```

แก้ไขการตั้งค่าใน `.env`:
```env
DATABASE_URL=mysql+pymysql://gps_user:your_password@localhost:3306/gps_track_db
DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_NAME=gps_track_db
DATABASE_USER=gps_user
DATABASE_PASSWORD=your_password
```

## 🛠️ Available Scripts

### System Scripts
- `./setup_venv.sh` - สร้าง virtual environment
- `./run_with_venv.sh` - รันระบบหลัก
- `./run_simulator_with_venv.sh` - รันระบบพร้อม simulator
- `./activate_venv.sh` - activate virtual environment

### Database Scripts
- `python setup_mariadb.py` - สร้างตารางฐานข้อมูล
- `python insert_sample_data.py` - เพิ่มข้อมูลตัวอย่าง
- `python view_sample_data.py` - ดูข้อมูลในฐานข้อมูล
- `python clear_sample_data.py` - ลบข้อมูลตัวอย่าง

### Installation Scripts
- `./install_dependencies_ubuntu.sh` - ติดตั้ง dependencies
- `./install_mariadb_ubuntu.sh` - ติดตั้ง MariaDB

## 🌐 Access URLs

เมื่อระบบทำงานแล้ว คุณสามารถเข้าถึงได้ที่:

- **Main Interface**: http://localhost:17890
- **API Documentation**: http://localhost:17890/docs
- **Health Check**: http://localhost:17890/health
- **API Status**: http://localhost:17890/api/status

## 🔧 Configuration

### Database Configuration
แก้ไขไฟล์ `.env`:
```env
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/database_name
```

### API Configuration
```env
API_HOST=0.0.0.0
API_PORT=17890
API_DEBUG=true
```

### Security Configuration
```env
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 🚨 Troubleshooting

### ปัญหาการติดตั้ง Dependencies
```bash
# อัปเดต pip
pip install --upgrade pip

# ติดตั้ง dependencies แยก
pip install fastapi uvicorn sqlalchemy pymysql
```

### ปัญหาการเชื่อมต่อฐานข้อมูล
```bash
# ตรวจสอบสถานะ MariaDB
sudo systemctl status mariadb

# เริ่ม MariaDB
sudo systemctl start mariadb

# ทดสอบการเชื่อมต่อ
mysql -u gps_user -p gps_track_db
```

### ปัญหา Port ถูกใช้งาน
```bash
# ตรวจสอบ port ที่ใช้งาน
sudo netstat -tlnp | grep 17890

# เปลี่ยน port ใน .env
API_PORT=8080
```

### ปัญหา Virtual Environment
```bash
# ลบ virtual environment เก่า
rm -rf venv

# สร้างใหม่
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 📊 Sample Data

ระบบมาพร้อมกับข้อมูลตัวอย่าง:

- **ยานพาหนะ**: 10 คัน (รถบรรทุก, รถตู้)
- **ข้อมูล GPS**: 400 รายการ
- **พื้นที่ที่กำหนด**: 10 พื้นที่
- **การแจ้งเตือน**: 15 รายการ
- **สถิติ Dashboard**: 16 รายการ

## 🔄 Updates

### อัปเดตโค้ด
```bash
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
```

### อัปเดตฐานข้อมูล
```bash
python setup_mariadb.py
python insert_sample_data.py
```

## 📝 Logs

ดู logs ได้ที่:
```bash
tail -f logs/gps_tracking.log
```

## 🆘 Support

หากมีปัญหาหรือต้องการความช่วยเหลือ:

1. ตรวจสอบ logs ใน `logs/gps_tracking.log`
2. ทดสอบ API endpoints ที่ `http://localhost:17890/docs`
3. ตรวจสอบการเชื่อมต่อฐานข้อมูล
4. ดู troubleshooting guide ข้างต้น

## 📄 License

โปรเจคนี้เป็น Open Source และสามารถใช้งานได้ฟรี
