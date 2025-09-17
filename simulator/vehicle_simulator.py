#!/usr/bin/env python3
"""
Vehicle GPS Simulator - สร้างรถจำลองที่ส่งข้อมูล GPS แบบเรียลไทม์
"""

import asyncio
import aiohttp
import random
import math
import time
from datetime import datetime, timedelta
from typing import List, Dict
import json

class VehicleSimulator:
    def __init__(self, vehicle_id: str, license_plate: str, vehicle_type: str, 
                 driver_name: str, start_lat: float, start_lng: float):
        self.vehicle_id = vehicle_id
        self.license_plate = license_plate
        self.vehicle_type = vehicle_type
        self.driver_name = driver_name
        
        # ตำแหน่งเริ่มต้น
        self.current_lat = start_lat
        self.current_lng = start_lng
        
        # สถานะการเดินทาง
        self.speed = random.uniform(20, 80)  # km/h
        self.heading = random.uniform(0, 360)  # degrees
        self.is_moving = True
        self.is_idle = False
        self.idle_start_time = None
        
        # เส้นทางการเดินทาง (จุดต่างๆ ในกรุงเทพฯ)
        self.route_points = [
            (13.7563, 100.5018),  # สยาม
            (13.7500, 100.5200),  # สีลม
            (13.7300, 100.5400),  # สาทร
            (13.7200, 100.5600),  # บางรัก
            (13.7000, 100.5800),  # สาทรใต้
            (13.6800, 100.6000),  # บางนา
            (13.6600, 100.6200),  # บางพลี
            (13.6400, 100.6400),  # บางบ่อ
            (13.6200, 100.6600),  # บางปะกง
            (13.6000, 100.6800),  # บางเสาธง
        ]
        
        self.current_route_index = 0
        self.target_lat, self.target_lng = self.route_points[0]
        
        # การตั้งค่า
        self.update_interval = random.uniform(10, 30)  # วินาที
        self.server_url = "http://localhost:17890"
        
    def calculate_distance(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """คำนวณระยะทางระหว่างสองจุด (km)"""
        R = 6371  # รัศมีโลก (km)
        
        dlat = math.radians(lat2 - lat1)
        dlng = math.radians(lng2 - lng1)
        
        a = (math.sin(dlat/2) * math.sin(dlat/2) + 
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
             math.sin(dlng/2) * math.sin(dlng/2))
        
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c
    
    def move_towards_target(self):
        """เคลื่อนที่ไปยังจุดเป้าหมาย"""
        if not self.is_moving:
            return
            
        # คำนวณระยะทางไปยังเป้าหมาย
        distance = self.calculate_distance(
            self.current_lat, self.current_lng,
            self.target_lat, self.target_lng
        )
        
        # ถ้าใกล้เป้าหมายแล้ว ให้ไปยังจุดถัดไป
        if distance < 0.5:  # 500 เมตร
            self.current_route_index = (self.current_route_index + 1) % len(self.route_points)
            self.target_lat, self.target_lng = self.route_points[self.current_route_index]
            distance = self.calculate_distance(
                self.current_lat, self.current_lng,
                self.target_lat, self.target_lng
            )
        
        # คำนวณทิศทาง
        lat_diff = self.target_lat - self.current_lat
        lng_diff = self.target_lng - self.current_lng
        
        # คำนวณระยะทางที่จะเคลื่อนที่ในครั้งนี้
        move_distance = (self.speed / 3600) * self.update_interval / 111.32  # แปลงเป็นองศา
        
        # คำนวณตำแหน่งใหม่
        if distance > 0:
            ratio = min(move_distance / distance, 1.0)
            self.current_lat += lat_diff * ratio
            self.current_lng += lng_diff * ratio
            
            # อัปเดตทิศทาง
            self.heading = math.degrees(math.atan2(lng_diff, lat_diff))
            
            # เพิ่มความแปรปรวนเล็กน้อย
            self.current_lat += random.uniform(-0.0001, 0.0001)
            self.current_lng += random.uniform(-0.0001, 0.0001)
    
    def simulate_idle_behavior(self):
        """จำลองพฤติกรรมการหยุดนิ่ง"""
        # มีโอกาส 5% ที่จะหยุดนิ่ง
        if random.random() < 0.05 and not self.is_idle:
            self.is_idle = True
            self.is_moving = False
            self.idle_start_time = datetime.now()
            self.speed = 0
            print(f"🚗 {self.vehicle_id} หยุดนิ่งที่ {self.current_lat:.6f}, {self.current_lng:.6f}")
        
        # ถ้าหยุดนิ่งแล้ว ให้หยุด 30-300 วินาที
        elif self.is_idle:
            idle_duration = (datetime.now() - self.idle_start_time).total_seconds()
            if idle_duration > random.uniform(30, 300):
                self.is_idle = False
                self.is_moving = True
                self.speed = random.uniform(20, 80)
                print(f"🚗 {self.vehicle_id} เริ่มเคลื่อนที่อีกครั้ง")
    
    async def send_gps_data(self, session: aiohttp.ClientSession):
        """ส่งข้อมูล GPS ไปยังเซิร์ฟเวอร์"""
        try:
            gps_data = {
                "vehicle_id": self.vehicle_id,
                "latitude": self.current_lat,
                "longitude": self.current_lng,
                "speed": self.speed,
                "heading": self.heading,
                "accuracy": random.uniform(3, 8),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            
            async with session.post(
                f"{self.server_url}/api/gps/data",
                json=gps_data,
                timeout=aiohttp.ClientTimeout(total=5)
            ) as response:
                if response.status == 200:
                    print(f"✅ {self.vehicle_id}: GPS data sent successfully")
                else:
                    print(f"❌ {self.vehicle_id}: Failed to send GPS data - {response.status}")
                    
        except Exception as e:
            print(f"❌ {self.vehicle_id}: Error sending GPS data - {e}")
    
    async def run(self, session: aiohttp.ClientSession):
        """รันการจำลองรถ"""
        print(f"🚗 Starting vehicle {self.vehicle_id} ({self.driver_name})")
        
        while True:
            try:
                # อัปเดตตำแหน่ง
                self.move_towards_target()
                self.simulate_idle_behavior()
                
                # ส่งข้อมูล GPS
                await self.send_gps_data(session)
                
                # รอตามช่วงเวลาที่กำหนด
                await asyncio.sleep(self.update_interval)
                
            except Exception as e:
                print(f"❌ {self.vehicle_id}: Error in simulation - {e}")
                await asyncio.sleep(5)

class FleetSimulator:
    def __init__(self):
        self.server_url = "http://localhost:17890"
        self.vehicles = []
        
    def create_fleet(self):
        """สร้างกองรถจำลอง"""
        vehicle_data = [
            ("V001", "กข-1234", "truck", "สมชาย ใจดี", 13.7563, 100.5018),
            ("V002", "กข-5678", "van", "สมหญิง รักดี", 13.7500, 100.5200),
            ("V003", "กข-9012", "motorcycle", "สมศักดิ์ เก่งดี", 13.7300, 100.5400),
            ("V004", "กข-3456", "car", "สมพร สวยดี", 13.7200, 100.5600),
            ("V005", "กข-7890", "bus", "สมบัติ ดีดี", 13.7000, 100.5800),
            ("V006", "กข-2468", "truck", "สมหมาย เก่งมาก", 13.6800, 100.6000),
            ("V007", "กข-1357", "van", "สมศรี สวยงาม", 13.6600, 100.6200),
            ("V008", "กข-9753", "motorcycle", "สมศักดิ์ เร็วมาก", 13.6400, 100.6400),
            ("V009", "กข-8642", "car", "สมพร ใจดี", 13.6200, 100.6600),
            ("V010", "กข-7531", "bus", "สมบัติ รักงาน", 13.6000, 100.6800),
        ]
        
        for vehicle_id, license_plate, vehicle_type, driver_name, start_lat, start_lng in vehicle_data:
            vehicle = VehicleSimulator(
                vehicle_id, license_plate, vehicle_type, driver_name, start_lat, start_lng
            )
            self.vehicles.append(vehicle)
        
        print(f"🚗 Created {len(self.vehicles)} vehicles")
    
    async def register_vehicles(self, session: aiohttp.ClientSession):
        """ลงทะเบียนรถในระบบ"""
        for vehicle in self.vehicles:
            try:
                vehicle_data = {
                    "vehicle_id": vehicle.vehicle_id,
                    "license_plate": vehicle.license_plate,
                    "vehicle_type": vehicle.vehicle_type,
                    "driver_name": vehicle.driver_name,
                    "driver_phone": f"08{random.randint(10000000, 99999999)}"
                }
                
                async with session.post(
                    f"{self.server_url}/api/vehicles/",
                    json=vehicle_data,
                    timeout=aiohttp.ClientTimeout(total=5)
                ) as response:
                    if response.status == 200:
                        print(f"✅ Registered vehicle {vehicle.vehicle_id}")
                    else:
                        print(f"❌ Failed to register vehicle {vehicle.vehicle_id} - {response.status}")
                        
            except Exception as e:
                print(f"❌ Error registering vehicle {vehicle.vehicle_id}: {e}")
    
    async def run_simulation(self):
        """รันการจำลองกองรถ"""
        print("=" * 60)
        print("🚗 GPS Vehicle Fleet Simulator")
        print("=" * 60)
        
        # สร้างกองรถ
        self.create_fleet()
        
        # เชื่อมต่อกับเซิร์ฟเวอร์
        async with aiohttp.ClientSession() as session:
            # ตรวจสอบว่าเซิร์ฟเวอร์ทำงานอยู่หรือไม่
            try:
                async with session.get(f"{self.server_url}/health", timeout=aiohttp.ClientTimeout(total=5)) as response:
                    if response.status == 200:
                        print("✅ Server is running")
                    else:
                        print("❌ Server is not responding properly")
                        return
            except Exception as e:
                print(f"❌ Cannot connect to server: {e}")
                print("Please make sure the GPS tracking server is running on port 17890")
                return
            
            # ลงทะเบียนรถ
            print("\n📝 Registering vehicles...")
            await self.register_vehicles(session)
            
            # รอสักครู่
            await asyncio.sleep(2)
            
            # เริ่มจำลองการเดินทาง
            print("\n🚀 Starting fleet simulation...")
            print("📍 Vehicles will start sending GPS data")
            print("🗺️  Open http://localhost:17890 to see the map")
            print("⏹️  Press Ctrl+C to stop")
            print("-" * 60)
            
            # รันรถทั้งหมดพร้อมกัน
            tasks = [vehicle.run(session) for vehicle in self.vehicles]
            await asyncio.gather(*tasks)

async def main():
    """Main function"""
    simulator = FleetSimulator()
    await simulator.run_simulation()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Simulation stopped by user")
    except Exception as e:
        print(f"\n❌ Simulation error: {e}")
