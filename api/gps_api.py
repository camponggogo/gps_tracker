from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import logging

from database.database import get_db
from database.models import GPSLog, Vehicle, Area, Alert
from api.schemas import (
    GPSData, GPSDataResponse, APIResponse, 
    VehicleLocation, PaginatedResponse
)
from config.settings import settings

router = APIRouter(prefix="/api/gps", tags=["GPS"])

@router.post("/data", response_model=APIResponse)
async def receive_gps_data(
    gps_data: GPSData,
    db: Session = Depends(get_db)
):
    """
    Receive GPS data from vehicles, mobile phones, or GPS devices
    """
    try:
        # Find vehicle by vehicle_id
        vehicle = db.query(Vehicle).filter(Vehicle.vehicle_id == gps_data.vehicle_id).first()
        if not vehicle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vehicle {gps_data.vehicle_id} not found"
            )
        
        # Check if vehicle is idle
        is_idle = False
        idle_duration = 0
        
        if gps_data.speed and gps_data.speed < 1.0:  # Less than 1 km/h
            # Get last GPS log to check idle duration
            last_log = db.query(GPSLog).filter(
                GPSLog.vehicle_id == vehicle.id
            ).order_by(GPSLog.timestamp.desc()).first()
            
            if last_log and last_log.is_idle:
                idle_duration = last_log.idle_duration + settings.gps_update_interval
            else:
                idle_duration = settings.gps_update_interval
            
            is_idle = idle_duration >= settings.gps_idle_timeout
        
        # Create GPS log entry
        gps_log = GPSLog(
            vehicle_id=vehicle.id,
            latitude=gps_data.latitude,
            longitude=gps_data.longitude,
            altitude=gps_data.altitude,
            speed=gps_data.speed,
            heading=gps_data.heading,
            accuracy=gps_data.accuracy,
            timestamp=gps_data.timestamp,
            is_idle=is_idle,
            idle_duration=idle_duration
        )
        
        db.add(gps_log)
        db.commit()
        db.refresh(gps_log)
        
        # Check for area violations
        await check_area_violations(vehicle.id, gps_data.latitude, gps_data.longitude, db)
        
        # Check for idle alerts
        if is_idle and idle_duration == settings.gps_idle_timeout:
            await create_idle_alert(vehicle.id, gps_data.latitude, gps_data.longitude, db)
        
        logging.info(f"GPS data received for vehicle {gps_data.vehicle_id}")
        
        return APIResponse(
            success=True,
            message="GPS data received successfully",
            data={"log_id": gps_log.id}
        )
        
    except Exception as e:
        logging.error(f"Error receiving GPS data: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing GPS data: {str(e)}"
        )

@router.get("/latest", response_model=List[VehicleLocation])
async def get_latest_vehicle_locations(
    db: Session = Depends(get_db),
    limit: int = 100
):
    """
    Get latest GPS locations for all vehicles
    """
    try:
        # Get latest GPS log for each vehicle
        latest_logs = db.query(GPSLog).join(Vehicle).filter(
            GPSLog.timestamp >= datetime.utcnow() - timedelta(hours=24)
        ).order_by(GPSLog.timestamp.desc()).limit(limit).all()
        
        locations = []
        for log in latest_logs:
            locations.append(VehicleLocation(
                vehicle_id=log.vehicle.vehicle_id,
                latitude=log.latitude,
                longitude=log.longitude,
                speed=log.speed,
                heading=log.heading,
                timestamp=log.timestamp,
                status=log.vehicle.status,
                is_idle=log.is_idle
            ))
        
        return locations
        
    except Exception as e:
        logging.error(f"Error getting latest locations: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving locations: {str(e)}"
        )

@router.get("/vehicle/{vehicle_id}/history", response_model=PaginatedResponse)
async def get_vehicle_gps_history(
    vehicle_id: str,
    db: Session = Depends(get_db),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    page: int = 1,
    size: int = 100
):
    """
    Get GPS history for a specific vehicle
    """
    try:
        # Find vehicle
        vehicle = db.query(Vehicle).filter(Vehicle.vehicle_id == vehicle_id).first()
        if not vehicle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vehicle {vehicle_id} not found"
            )
        
        # Build query
        query = db.query(GPSLog).filter(GPSLog.vehicle_id == vehicle.id)
        
        if start_date:
            query = query.filter(GPSLog.timestamp >= start_date)
        if end_date:
            query = query.filter(GPSLog.timestamp <= end_date)
        
        # Get total count
        total = query.count()
        
        # Get paginated results
        logs = query.order_by(GPSLog.timestamp.desc()).offset(
            (page - 1) * size
        ).limit(size).all()
        
        # Convert to response format
        items = []
        for log in logs:
            items.append(GPSDataResponse(
                id=log.id,
                vehicle_id=vehicle.vehicle_id,
                latitude=log.latitude,
                longitude=log.longitude,
                altitude=log.altitude,
                speed=log.speed,
                heading=log.heading,
                accuracy=log.accuracy,
                timestamp=log.timestamp,
                is_idle=log.is_idle,
                idle_duration=log.idle_duration
            ))
        
        return PaginatedResponse(
            items=items,
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size
        )
        
    except Exception as e:
        logging.error(f"Error getting vehicle history: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving vehicle history: {str(e)}"
        )

async def check_area_violations(vehicle_id: int, latitude: float, longitude: float, db: Session):
    """
    Check if vehicle is violating any area rules
    """
    try:
        # Get all active areas
        areas = db.query(Area).filter(Area.is_active == True).all()
        
        for area in areas:
            # Check if vehicle is in area (simplified check)
            if is_point_in_area(latitude, longitude, area.coordinates, area.shape):
                # Create alert if vehicle enters restricted area
                if area.area_type in [AreaType.ALERT, AreaType.CRITICAL]:
                    alert = Alert(
                        vehicle_id=vehicle_id,
                        area_id=area.id,
                        alert_type=f"area_violation_{area.area_type.value}",
                        message=f"Vehicle entered {area.area_type.value} area: {area.name}",
                        latitude=latitude,
                        longitude=longitude
                    )
                    db.add(alert)
        
        db.commit()
        
    except Exception as e:
        logging.error(f"Error checking area violations: {e}")
        db.rollback()

async def create_idle_alert(vehicle_id: int, latitude: float, longitude: float, db: Session):
    """
    Create alert for vehicle being idle too long
    """
    try:
        alert = Alert(
            vehicle_id=vehicle_id,
            alert_type="idle_timeout",
            message=f"Vehicle has been idle for {settings.gps_idle_timeout} seconds",
            latitude=latitude,
            longitude=longitude
        )
        db.add(alert)
        db.commit()
        
    except Exception as e:
        logging.error(f"Error creating idle alert: {e}")
        db.rollback()

def is_point_in_area(lat: float, lon: float, coordinates: dict, shape: str) -> bool:
    """
    Check if a point is inside an area (simplified implementation)
    """
    # This is a simplified implementation
    # In production, you would use proper geometric calculations
    if shape == "circle":
        center_lat = coordinates.get("center", {}).get("lat", 0)
        center_lon = coordinates.get("center", {}).get("lng", 0)
        radius = coordinates.get("radius", 0)
        
        # Calculate distance (simplified)
        distance = ((lat - center_lat) ** 2 + (lon - center_lon) ** 2) ** 0.5
        return distance <= radius
    
    elif shape == "polygon":
        # Implement polygon point-in-polygon algorithm
        # For now, return False
        return False
    
    elif shape == "rectangle":
        bounds = coordinates.get("bounds", {})
        min_lat = bounds.get("south", 0)
        max_lat = bounds.get("north", 0)
        min_lon = bounds.get("west", 0)
        max_lon = bounds.get("east", 0)
        
        return min_lat <= lat <= max_lat and min_lon <= lon <= max_lon
    
    return False
