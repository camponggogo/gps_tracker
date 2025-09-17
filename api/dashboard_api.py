from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List, Optional
from datetime import datetime, timedelta

from database.database import get_db
from database.models import (
    Vehicle, GPSLog, Area, Alert, Route, 
    VehicleType, VehicleStatus, AreaType
)
from api.schemas import (
    DashboardStats, VehicleLocation, APIResponse
)

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats(
    db: Session = Depends(get_db)
):
    """
    Get dashboard statistics
    """
    try:
        # Get vehicle counts by status
        vehicle_counts = db.query(
            Vehicle.status,
            func.count(Vehicle.id)
        ).group_by(Vehicle.status).all()
        
        total_vehicles = db.query(Vehicle).count()
        active_vehicles = 0
        inactive_vehicles = 0
        maintenance_vehicles = 0
        breakdown_vehicles = 0
        
        for status, count in vehicle_counts:
            if status == VehicleStatus.ACTIVE:
                active_vehicles = count
            elif status == VehicleStatus.INACTIVE:
                inactive_vehicles = count
            elif status == VehicleStatus.MAINTENANCE:
                maintenance_vehicles = count
            elif status == VehicleStatus.BREAKDOWN:
                breakdown_vehicles = count
        
        # Get average speed from recent GPS logs
        recent_time = datetime.utcnow() - timedelta(hours=1)
        avg_speed_result = db.query(
            func.avg(GPSLog.speed)
        ).filter(
            and_(
                GPSLog.timestamp >= recent_time,
                GPSLog.speed.isnot(None),
                GPSLog.speed > 0
            )
        ).scalar()
        
        average_speed = float(avg_speed_result) if avg_speed_result else 0.0
        
        # Get vehicles in checkpoint areas
        checkpoint_areas = db.query(Area).filter(
            Area.area_type == AreaType.CHECKPOINT,
            Area.is_active == True
        ).all()
        
        vehicles_in_checkpoint = 0
        for area in checkpoint_areas:
            # Get latest GPS logs for each vehicle
            latest_logs = db.query(GPSLog).join(Vehicle).filter(
                GPSLog.timestamp >= datetime.utcnow() - timedelta(minutes=5)
            ).all()
            
            for log in latest_logs:
                if is_point_in_area(log.latitude, log.longitude, area.coordinates, area.shape):
                    vehicles_in_checkpoint += 1
                    break
        
        # Get vehicles delivered (completed routes in last 24 hours)
        delivered_vehicles = db.query(Route).filter(
            Route.end_time >= datetime.utcnow() - timedelta(hours=24),
            Route.end_time.isnot(None)
        ).count()
        
        # Get vehicles loading (in checkpoint areas)
        vehicles_loading = vehicles_in_checkpoint
        
        return DashboardStats(
            total_vehicles=total_vehicles,
            active_vehicles=active_vehicles,
            inactive_vehicles=inactive_vehicles,
            maintenance_vehicles=maintenance_vehicles,
            breakdown_vehicles=breakdown_vehicles,
            average_speed=average_speed,
            vehicles_in_checkpoint=vehicles_in_checkpoint,
            vehicles_delivered=delivered_vehicles,
            vehicles_loading=vehicles_loading
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving dashboard stats: {str(e)}"
        )

@router.get("/vehicle-locations", response_model=List[VehicleLocation])
async def get_vehicle_locations(
    db: Session = Depends(get_db),
    vehicle_type: Optional[VehicleType] = None,
    status: Optional[VehicleStatus] = None
):
    """
    Get current vehicle locations for map display
    """
    try:
        # Build query for latest GPS logs
        query = db.query(GPSLog).join(Vehicle).filter(
            GPSLog.timestamp >= datetime.utcnow() - timedelta(hours=24)
        )
        
        if vehicle_type:
            query = query.filter(Vehicle.vehicle_type == vehicle_type)
        
        if status:
            query = query.filter(Vehicle.status == status)
        
        # Get latest log for each vehicle
        latest_logs = query.order_by(
            Vehicle.id, GPSLog.timestamp.desc()
        ).distinct(Vehicle.id).all()
        
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
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving vehicle locations: {str(e)}"
        )

@router.get("/alerts", response_model=List[dict])
async def get_recent_alerts(
    db: Session = Depends(get_db),
    limit: int = 50,
    resolved: Optional[bool] = None
):
    """
    Get recent alerts
    """
    try:
        query = db.query(Alert).join(Vehicle)
        
        if resolved is not None:
            query = query.filter(Alert.is_resolved == resolved)
        
        alerts = query.order_by(Alert.created_at.desc()).limit(limit).all()
        
        alert_list = []
        for alert in alerts:
            alert_list.append({
                "id": alert.id,
                "vehicle_id": alert.vehicle.vehicle_id,
                "vehicle_name": alert.vehicle.license_plate or alert.vehicle.vehicle_id,
                "alert_type": alert.alert_type,
                "message": alert.message,
                "latitude": alert.latitude,
                "longitude": alert.longitude,
                "is_resolved": alert.is_resolved,
                "created_at": alert.created_at,
                "resolved_at": alert.resolved_at
            })
        
        return alert_list
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving alerts: {str(e)}"
        )

@router.get("/vehicle-types-stats", response_model=dict)
async def get_vehicle_types_stats(
    db: Session = Depends(get_db)
):
    """
    Get statistics by vehicle type
    """
    try:
        # Get vehicle counts by type
        type_counts = db.query(
            Vehicle.vehicle_type,
            func.count(Vehicle.id)
        ).group_by(Vehicle.vehicle_type).all()
        
        # Get average speeds by type
        recent_time = datetime.utcnow() - timedelta(hours=1)
        speed_stats = db.query(
            Vehicle.vehicle_type,
            func.avg(GPSLog.speed),
            func.max(GPSLog.speed),
            func.min(GPSLog.speed)
        ).join(GPSLog).filter(
            and_(
                GPSLog.timestamp >= recent_time,
                GPSLog.speed.isnot(None),
                GPSLog.speed > 0
            )
        ).group_by(Vehicle.vehicle_type).all()
        
        stats = {}
        for vehicle_type, count in type_counts:
            stats[vehicle_type.value] = {
                "count": count,
                "average_speed": 0.0,
                "max_speed": 0.0,
                "min_speed": 0.0
            }
        
        for vehicle_type, avg_speed, max_speed, min_speed in speed_stats:
            if vehicle_type.value in stats:
                stats[vehicle_type.value].update({
                    "average_speed": float(avg_speed) if avg_speed else 0.0,
                    "max_speed": float(max_speed) if max_speed else 0.0,
                    "min_speed": float(min_speed) if min_speed else 0.0
                })
        
        return stats
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving vehicle type stats: {str(e)}"
        )

@router.get("/area-stats", response_model=dict)
async def get_area_stats(
    db: Session = Depends(get_db)
):
    """
    Get statistics for areas
    """
    try:
        # Get area counts by type
        area_counts = db.query(
            Area.area_type,
            func.count(Area.id)
        ).filter(Area.is_active == True).group_by(Area.area_type).all()
        
        # Get vehicles currently in each area type
        recent_time = datetime.utcnow() - timedelta(minutes=5)
        vehicles_in_areas = {}
        
        for area_type, count in area_counts:
            areas = db.query(Area).filter(
                Area.area_type == area_type,
                Area.is_active == True
            ).all()
            
            vehicles_in_area = 0
            for area in areas:
                latest_logs = db.query(GPSLog).join(Vehicle).filter(
                    GPSLog.timestamp >= recent_time
                ).all()
                
                for log in latest_logs:
                    if is_point_in_area(log.latitude, log.longitude, area.coordinates, area.shape):
                        vehicles_in_area += 1
                        break
            
            vehicles_in_areas[area_type.value] = {
                "total_areas": count,
                "vehicles_inside": vehicles_in_area
            }
        
        return vehicles_in_areas
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving area stats: {str(e)}"
        )

def is_point_in_area(lat: float, lon: float, coordinates: dict, shape: str) -> bool:
    """
    Check if a point is inside an area (simplified implementation)
    """
    try:
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
        
    except Exception:
        return False
