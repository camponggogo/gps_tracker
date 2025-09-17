# GPS Area Tracking System - Virtual Environment Guide

## 🐍 การใช้ Virtual Environment

Virtual Environment ช่วยแยก dependencies ของโปรเจคนี้จากระบบ Python หลัก ทำให้หลีกเลี่ยงปัญหา conflicts และง่ายต่อการจัดการ

## 🚀 วิธีการใช้งาน

### 1. ติดตั้งครั้งแรก (Setup)
```bash
# Windows
setup_venv.bat
```

### 2. รันระบบ
```bash
# วิธีที่ 1: รันพร้อมกัน
run_with_venv.bat

# วิธีที่ 2: รันแยกกัน
activate_venv.bat
python run.py
```

### 3. รันพร้อม Simulator
```bash
run_simulator_with_venv.bat
```

## 📁 โครงสร้าง Virtual Environment

```
gps_area_tracking/
├── venv/                    # Virtual environment
│   ├── Scripts/            # Windows scripts
│   ├── Lib/                # Python libraries
│   └── pyvenv.cfg          # Configuration
├── setup_venv.bat          # Setup script
├── activate_venv.bat       # Activation script
├── run_with_venv.bat       # Run with venv
└── run_simulator_with_venv.bat
```

## 🔧 คำสั่งที่สำคัญ

### Windows
```bash
# สร้าง virtual environment
python -m venv venv

# เปิดใช้งาน
venv\Scripts\activate.bat

# ปิดใช้งาน
deactivate

# ติดตั้ง dependencies
pip install -r requirements.txt
```

### Linux/Mac
```bash
# สร้าง virtual environment
python -m venv venv

# เปิดใช้งาน
source venv/bin/activate

# ปิดใช้งาน
deactivate
```

## 📦 Dependencies ที่ติดตั้ง

### Core Dependencies
- fastapi==0.104.1
- uvicorn==0.24.0
- sqlalchemy==2.0.23
- pymysql==1.1.0
- python-multipart==0.0.6
- python-jose[cryptography]==3.3.0
- passlib[bcrypt]==1.7.4
- python-dotenv==1.0.0
- pydantic==2.5.0
- pydantic-settings==2.1.0
- httpx==0.25.2
- jinja2==3.1.2
- aiofiles==23.2.1
- python-dateutil==2.8.2
- pytz==2023.3
- requests==2.31.0

### Simulator Dependencies
- aiohttp==3.9.1

## 🎯 ข้อดีของการใช้ Virtual Environment

### ✅ ข้อดี
- **แยก dependencies**: ไม่กระทบระบบ Python หลัก
- **หลีกเลี่ยง conflicts**: แต่ละโปรเจคมี dependencies แยกกัน
- **ง่ายต่อการจัดการ**: ติดตั้ง/ลบ dependencies ได้ง่าย
- **Reproducible**: สามารถสร้าง environment เดียวกันได้ทุกที่
- **Clean**: ไม่มี packages ที่ไม่จำเป็น

### ❌ ข้อเสีย
- **ใช้พื้นที่**: ต้องใช้พื้นที่เก็บ packages ซ้ำ
- **ต้องจำ**: ต้องจำเปิดใช้งานก่อนรันโปรแกรม

## 🔧 การแก้ไขปัญหา

### Virtual Environment ไม่ทำงาน
```bash
# ลบและสร้างใหม่
rmdir /s /q venv
python -m venv venv
```

### Dependencies ไม่ติดตั้ง
```bash
# อัปเกรด pip ก่อน
python -m pip install --upgrade pip

# ติดตั้งใหม่
pip install -r requirements.txt
```

### Python ไม่พบ
```bash
# ตรวจสอบ Python
python --version

# ตรวจสอบ PATH
where python
```

## 📋 Best Practices

### 1. ใช้ Virtual Environment เสมอ
- สำหรับทุกโปรเจค Python
- แยก dependencies ให้ชัดเจน

### 2. เก็บ requirements.txt
- บันทึก dependencies ที่ใช้
- อัปเดตเมื่อเพิ่ม/ลบ packages

### 3. ใช้ .gitignore
```
venv/
__pycache__/
*.pyc
.env
```

### 4. เอกสารการติดตั้ง
- บันทึกขั้นตอนการติดตั้ง
- อัปเดตเมื่อมีการเปลี่ยนแปลง

## 🚀 การใช้งานจริง

### เริ่มต้นใหม่
```bash
# 1. Clone หรือ download โปรเจค
# 2. รัน setup
setup_venv.bat

# 3. รันระบบ
run_with_venv.bat
```

### พัฒนาต่อ
```bash
# 1. เปิดใช้งาน venv
activate_venv.bat

# 2. ติดตั้ง packages เพิ่มเติม
pip install package_name

# 3. อัปเดต requirements.txt
pip freeze > requirements.txt

# 4. รันโปรแกรม
python run.py
```

## 📞 การสนับสนุน

หากมีปัญหาหรือต้องการความช่วยเหลือ:
1. ตรวจสอบ Python version (ต้องเป็น 3.8+)
2. ตรวจสอบการเชื่อมต่ออินเทอร์เน็ต
3. ลองสร้าง virtual environment ใหม่
4. ตรวจสอบ logs ใน `logs/gps_tracking.log`
