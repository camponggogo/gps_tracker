# GPS Area Tracking System

ระบบติดตาม GPS แบบเรียลไทม์พร้อมการจัดการพื้นที่และ Dashboard แบบครบวงจร

## คุณสมบัติหลัก

### 🚗 การติดตามยานพาหนะ
- รับข้อมูล GPS จากอุปกรณ์ติดรถ, มือถือ, หรือ GPS นำทาง
- แสดงตำแหน่งยานพาหนะแบบเรียลไทม์บนแผนที่
- ติดตามเส้นทางการเดินทาง (Route Tracking)
- แจ้งเตือนเมื่อรถหยุดนิ่งเกินเวลาที่กำหนด

### 🗺️ การจัดการพื้นที่
- **Entrance Area**: พื้นที่ทางเข้า
- **Alert Area**: พื้นที่แจ้งเตือน
- **Critical Area**: พื้นที่วิกฤต
- **Checkpoint Area**: พื้นที่จุดตรวจ (คลังสินค้า)
- รองรับการสร้างพื้นที่แบบ Polygon, Circle, Rectangle
- กำหนด Buffer Distance สำหรับแต่ละพื้นที่

### 📊 Dashboard
- แสดงจำนวนรถแต่ละประเภท
- อัตราเร็วเฉลี่ย
- จำนวนรถ Active/Inactive/Maintenance/Breakdown
- จำนวนรถที่อยู่ใน Checkpoint Area (กำลังยกของ)
- จำนวนรถที่ส่งของเสร็จแล้ว
- แสดงข้อมูลแบบเรียลไทม์

### 📈 ระบบรายงาน
- รายงานสรุปผลการติดตาม
- สามารถคัดกรองรายงานตามช่วงเวลา, ประเภทรถ, พื้นที่
- Export ข้อมูลเป็น CSV/Excel

## เทคโนโลยีที่ใช้

- **Backend**: FastAPI (Python)
- **Database**: MariaDB/MySQL
- **Frontend**: HTML5, CSS3, JavaScript
- **Map**: Leaflet (OpenStreetMap)
- **Real-time**: WebSocket
- **Authentication**: JWT

## การติดตั้ง

### 1. ติดตั้ง Dependencies

```bash
pip install -r requirements.txt
```

### 2. ตั้งค่าฐานข้อมูล

สร้างฐานข้อมูล MariaDB/MySQL:

```sql
-- ใช้ MariaDB/MySQL ที่มีอยู่แล้ว
-- Database: transportation_db (ตาม config.ini)
-- User: root
-- Password: 123456!

-- รันไฟล์ setup
mysql -u root -p123456! < database/mariadb_setup.sql
```

### 3. ตั้งค่า Environment Variables

คัดลอกไฟล์ `env.example` เป็น `.env` และแก้ไขค่าต่างๆ:

```bash
cp env.example .env
```

แก้ไขค่าต่างๆ ในไฟล์ `.env`:

```env
DATABASE_URL=mysql+pymysql://root:123456!@localhost:3306/transportation_db
SECRET_KEY=your-secret-key-here
```

### 4. รันระบบ

```bash
python main.py
```

ระบบจะรันที่ `http://localhost:17890`

## การใช้งาน

### 1. เพิ่มยานพาหนะ

ใช้ API หรือ Web Interface เพื่อเพิ่มยานพาหนะ:

```bash
curl -X POST "http://localhost:17890/api/vehicles/" \
  -H "Content-Type: application/json" \
  -d '{
    "vehicle_id": "V001",
    "license_plate": "กข-1234",
    "vehicle_type": "truck",
    "driver_name": "สมชาย ใจดี",
    "driver_phone": "0812345678"
  }'
```

### 2. ส่งข้อมูล GPS

ส่งข้อมูล GPS จากอุปกรณ์:

```bash
curl -X POST "http://localhost:17890/api/gps/data" \
  -H "Content-Type: application/json" \
  -d '{
    "vehicle_id": "V001",
    "latitude": 13.7563,
    "longitude": 100.5018,
    "speed": 45.5,
    "heading": 180,
    "accuracy": 5.0,
    "timestamp": "2024-01-01T10:00:00Z"
  }'
```

### 3. สร้างพื้นที่

ใช้ Web Interface เพื่อสร้างพื้นที่บนแผนที่:

1. เปิด `http://localhost:17890`
2. คลิก "Add Area"
3. เลือกประเภทพื้นที่
4. วาดพื้นที่บนแผนที่
5. กรอกข้อมูลและบันทึก

## API Endpoints

### GPS Data
- `POST /api/gps/data` - ส่งข้อมูล GPS
- `GET /api/gps/latest` - ข้อมูลตำแหน่งล่าสุด
- `GET /api/gps/vehicle/{vehicle_id}/history` - ประวัติการเดินทาง

### Vehicles
- `GET /api/vehicles/` - รายการยานพาหนะ
- `POST /api/vehicles/` - เพิ่มยานพาหนะ
- `GET /api/vehicles/{vehicle_id}` - ข้อมูลยานพาหนะ
- `PUT /api/vehicles/{vehicle_id}` - แก้ไขยานพาหนะ
- `DELETE /api/vehicles/{vehicle_id}` - ลบยานพาหนะ

### Areas
- `GET /api/areas/` - รายการพื้นที่
- `POST /api/areas/` - สร้างพื้นที่
- `GET /api/areas/{area_id}` - ข้อมูลพื้นที่
- `PUT /api/areas/{area_id}` - แก้ไขพื้นที่
- `DELETE /api/areas/{area_id}` - ลบพื้นที่

### Dashboard
- `GET /api/dashboard/stats` - สถิติ Dashboard
- `GET /api/dashboard/vehicle-locations` - ตำแหน่งยานพาหนะ
- `GET /api/dashboard/alerts` - การแจ้งเตือน
- `GET /api/dashboard/vehicle-types-stats` - สถิติตามประเภทรถ

## โครงสร้างโปรเจค

```
gps_area_tracking/
├── api/                    # API endpoints
│   ├── gps_api.py         # GPS data API
│   ├── vehicle_api.py     # Vehicle management API
│   ├── area_api.py        # Area management API
│   ├── dashboard_api.py   # Dashboard API
│   └── schemas.py         # Pydantic schemas
├── database/              # Database related
│   ├── models.py          # SQLAlchemy models
│   └── database.py        # Database connection
├── static/                # Static files
│   ├── css/
│   │   └── map.css        # Map styles
│   └── js/
│       └── map.js         # Map JavaScript
├── templates/             # HTML templates
│   └── map.html          # Main map page
├── config/                # Configuration
│   └── settings.py        # App settings
├── logs/                  # Log files
├── uploads/               # Upload directory
├── main.py               # Main application
├── requirements.txt      # Python dependencies
├── env.example          # Environment variables example
└── README.md            # This file
```

## การพัฒนาต่อ

### เพิ่มฟีเจอร์ใหม่
1. สร้าง API endpoint ใน `api/` directory
2. เพิ่ม model ใน `database/models.py` ถ้าจำเป็น
3. อัปเดต frontend ใน `static/js/map.js`
4. เพิ่ม CSS ใน `static/css/map.css`

### การ Debug
- เปิด Debug mode ใน `.env`: `API_DEBUG=true`
- ดู logs ใน `logs/gps_tracking.log`
- ใช้ FastAPI docs ที่ `http://localhost:17890/docs`

## การสนับสนุน

หากมีปัญหาหรือต้องการความช่วยเหลือ:

1. ตรวจสอบ logs ใน `logs/gps_tracking.log`
2. ตรวจสอบการเชื่อมต่อฐานข้อมูล
3. ตรวจสอบ Environment variables
4. ดู FastAPI docs ที่ `/docs`

## License

MIT License - ใช้งานได้ฟรีและปรับแต่งได้ตามต้องการ
