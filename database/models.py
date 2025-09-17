from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import JSON
from datetime import datetime
import enum

Base = declarative_base()

class VehicleType(enum.Enum):
    TRUCK = "truck"
    VAN = "van"
    MOTORCYCLE = "motorcycle"
    CAR = "car"
    BUS = "bus"

class VehicleStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"
    BREAKDOWN = "breakdown"

class AreaType(enum.Enum):
    ENTRANCE = "entrance"
    ALERT = "alert"
    CRITICAL = "critical"
    CHECKPOINT = "checkpoint"

class AreaShape(enum.Enum):
    POLYGON = "polygon"
    CIRCLE = "circle"
    RECTANGLE = "rectangle"

class Vehicle(Base):
    __tablename__ = "vehicles"
    
    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(String(50), unique=True, index=True, nullable=False)
    license_plate = Column(String(20), unique=True, index=True)
    vehicle_type = Column(Enum(VehicleType), nullable=False)
    status = Column(Enum(VehicleStatus), default=VehicleStatus.ACTIVE)
    driver_name = Column(String(100))
    driver_phone = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    gps_logs = relationship("GPSLog", back_populates="vehicle")
    alerts = relationship("Alert", back_populates="vehicle")

class GPSLog(Base):
    __tablename__ = "gps_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    altitude = Column(Float)
    speed = Column(Float)  # km/h
    heading = Column(Float)  # degrees
    accuracy = Column(Float)  # meters
    timestamp = Column(DateTime, nullable=False, index=True)
    is_idle = Column(Boolean, default=False)
    idle_duration = Column(Integer, default=0)  # seconds
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    vehicle = relationship("Vehicle", back_populates="gps_logs")

class Area(Base):
    __tablename__ = "areas"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    area_type = Column(Enum(AreaType), nullable=False)
    shape = Column(Enum(AreaShape), nullable=False)
    coordinates = Column(JSON, nullable=False)  # Store coordinates as JSON
    buffer_distance = Column(Float, default=0.0)  # meters
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    alerts = relationship("Alert", back_populates="area")

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    area_id = Column(Integer, ForeignKey("areas.id"), nullable=True)
    alert_type = Column(String(50), nullable=False)
    message = Column(Text, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    is_resolved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime)
    
    # Relationships
    vehicle = relationship("Vehicle", back_populates="alerts")
    area = relationship("Area", back_populates="alerts")

class Route(Base):
    __tablename__ = "routes"
    
    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    start_latitude = Column(Float, nullable=False)
    start_longitude = Column(Float, nullable=False)
    end_latitude = Column(Float, nullable=False)
    end_longitude = Column(Float, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    total_distance = Column(Float)  # km
    total_duration = Column(Integer)  # seconds
    average_speed = Column(Float)  # km/h
    max_speed = Column(Float)  # km/h
    idle_time = Column(Integer, default=0)  # seconds
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    vehicle = relationship("Vehicle")

class DashboardStats(Base):
    __tablename__ = "dashboard_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    stat_type = Column(String(50), nullable=False)
    stat_value = Column(Float, nullable=False)
    stat_label = Column(String(100))
    timestamp = Column(DateTime, default=datetime.utcnow)
    meta_data = Column(JSON)  # Additional data as JSON
