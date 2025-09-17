from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from database.models import VehicleType, VehicleStatus, AreaType, AreaShape

# GPS Data Schemas
class GPSData(BaseModel):
    vehicle_id: str = Field(..., description="Vehicle ID")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude")
    altitude: Optional[float] = Field(None, description="Altitude in meters")
    speed: Optional[float] = Field(None, ge=0, description="Speed in km/h")
    heading: Optional[float] = Field(None, ge=0, le=360, description="Heading in degrees")
    accuracy: Optional[float] = Field(None, ge=0, description="Accuracy in meters")
    timestamp: datetime = Field(..., description="GPS timestamp")

class GPSDataResponse(BaseModel):
    id: int
    vehicle_id: str
    latitude: float
    longitude: float
    altitude: Optional[float]
    speed: Optional[float]
    heading: Optional[float]
    accuracy: Optional[float]
    timestamp: datetime
    is_idle: bool
    idle_duration: int

# Vehicle Schemas
class VehicleCreate(BaseModel):
    vehicle_id: str = Field(..., description="Unique vehicle identifier")
    license_plate: Optional[str] = Field(None, description="License plate number")
    vehicle_type: VehicleType = Field(..., description="Type of vehicle")
    driver_name: Optional[str] = Field(None, description="Driver name")
    driver_phone: Optional[str] = Field(None, description="Driver phone number")

class VehicleUpdate(BaseModel):
    license_plate: Optional[str] = None
    vehicle_type: Optional[VehicleType] = None
    status: Optional[VehicleStatus] = None
    driver_name: Optional[str] = None
    driver_phone: Optional[str] = None

class VehicleResponse(BaseModel):
    id: int
    vehicle_id: str
    license_plate: Optional[str]
    vehicle_type: VehicleType
    status: VehicleStatus
    driver_name: Optional[str]
    driver_phone: Optional[str]
    created_at: datetime
    updated_at: datetime

# Area Schemas
class AreaCreate(BaseModel):
    name: str = Field(..., description="Area name")
    area_type: AreaType = Field(..., description="Type of area")
    shape: AreaShape = Field(..., description="Shape of area")
    coordinates: Dict[str, Any] = Field(..., description="Area coordinates")
    buffer_distance: Optional[float] = Field(0.0, description="Buffer distance in meters")

class AreaUpdate(BaseModel):
    name: Optional[str] = None
    area_type: Optional[AreaType] = None
    shape: Optional[AreaShape] = None
    coordinates: Optional[Dict[str, Any]] = None
    buffer_distance: Optional[float] = None
    is_active: Optional[bool] = None

class AreaResponse(BaseModel):
    id: int
    name: str
    area_type: AreaType
    shape: AreaShape
    coordinates: Dict[str, Any]
    buffer_distance: float
    is_active: bool
    created_at: datetime
    updated_at: datetime

# Alert Schemas
class AlertResponse(BaseModel):
    id: int
    vehicle_id: int
    area_id: Optional[int]
    alert_type: str
    message: str
    latitude: Optional[float]
    longitude: Optional[float]
    is_resolved: bool
    created_at: datetime
    resolved_at: Optional[datetime]

# Route Schemas
class RouteResponse(BaseModel):
    id: int
    vehicle_id: int
    start_latitude: float
    start_longitude: float
    end_latitude: float
    end_longitude: float
    start_time: datetime
    end_time: Optional[datetime]
    total_distance: Optional[float]
    total_duration: Optional[int]
    average_speed: Optional[float]
    max_speed: Optional[float]
    idle_time: int

# Dashboard Schemas
class DashboardStats(BaseModel):
    total_vehicles: int
    active_vehicles: int
    inactive_vehicles: int
    maintenance_vehicles: int
    breakdown_vehicles: int
    average_speed: float
    vehicles_in_checkpoint: int
    vehicles_delivered: int
    vehicles_loading: int

class VehicleLocation(BaseModel):
    vehicle_id: str
    latitude: float
    longitude: float
    speed: Optional[float]
    heading: Optional[float]
    timestamp: datetime
    status: VehicleStatus
    is_idle: bool

# Report Schemas
class ReportFilter(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    vehicle_ids: Optional[List[str]] = None
    vehicle_types: Optional[List[VehicleType]] = None
    area_ids: Optional[List[int]] = None
    include_idle: Optional[bool] = True

class ReportResponse(BaseModel):
    report_type: str
    generated_at: datetime
    filters: ReportFilter
    data: Dict[str, Any]
    summary: Dict[str, Any]

# API Response Schemas
class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None

class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    size: int
    pages: int
