from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from database.database import get_db
from database.models import Vehicle, VehicleType, VehicleStatus
from api.schemas import (
    VehicleCreate, VehicleUpdate, VehicleResponse, 
    APIResponse, PaginatedResponse
)

router = APIRouter(prefix="/api/vehicles", tags=["Vehicles"])

@router.post("/", response_model=VehicleResponse)
async def create_vehicle(
    vehicle_data: VehicleCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new vehicle
    """
    try:
        # Check if vehicle_id already exists
        existing_vehicle = db.query(Vehicle).filter(
            Vehicle.vehicle_id == vehicle_data.vehicle_id
        ).first()
        
        if existing_vehicle:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Vehicle with ID {vehicle_data.vehicle_id} already exists"
            )
        
        # Check if license_plate already exists
        if vehicle_data.license_plate:
            existing_plate = db.query(Vehicle).filter(
                Vehicle.license_plate == vehicle_data.license_plate
            ).first()
            
            if existing_plate:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Vehicle with license plate {vehicle_data.license_plate} already exists"
                )
        
        # Create new vehicle
        vehicle = Vehicle(
            vehicle_id=vehicle_data.vehicle_id,
            license_plate=vehicle_data.license_plate,
            vehicle_type=vehicle_data.vehicle_type,
            driver_name=vehicle_data.driver_name,
            driver_phone=vehicle_data.driver_phone,
            status=VehicleStatus.ACTIVE
        )
        
        db.add(vehicle)
        db.commit()
        db.refresh(vehicle)
        
        return VehicleResponse(
            id=vehicle.id,
            vehicle_id=vehicle.vehicle_id,
            license_plate=vehicle.license_plate,
            vehicle_type=vehicle.vehicle_type,
            status=vehicle.status,
            driver_name=vehicle.driver_name,
            driver_phone=vehicle.driver_phone,
            created_at=vehicle.created_at,
            updated_at=vehicle.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating vehicle: {str(e)}"
        )

@router.get("/", response_model=PaginatedResponse)
async def get_vehicles(
    db: Session = Depends(get_db),
    vehicle_type: Optional[VehicleType] = None,
    status: Optional[VehicleStatus] = None,
    page: int = 1,
    size: int = 50
):
    """
    Get list of vehicles with optional filtering
    """
    try:
        # Build query
        query = db.query(Vehicle)
        
        if vehicle_type:
            query = query.filter(Vehicle.vehicle_type == vehicle_type)
        
        if status:
            query = query.filter(Vehicle.status == status)
        
        # Get total count
        total = query.count()
        
        # Get paginated results
        vehicles = query.order_by(Vehicle.created_at.desc()).offset(
            (page - 1) * size
        ).limit(size).all()
        
        # Convert to response format
        items = []
        for vehicle in vehicles:
            items.append(VehicleResponse(
                id=vehicle.id,
                vehicle_id=vehicle.vehicle_id,
                license_plate=vehicle.license_plate,
                vehicle_type=vehicle.vehicle_type,
                status=vehicle.status,
                driver_name=vehicle.driver_name,
                driver_phone=vehicle.driver_phone,
                created_at=vehicle.created_at,
                updated_at=vehicle.updated_at
            ))
        
        return PaginatedResponse(
            items=items,
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving vehicles: {str(e)}"
        )

@router.get("/{vehicle_id}", response_model=VehicleResponse)
async def get_vehicle(
    vehicle_id: str,
    db: Session = Depends(get_db)
):
    """
    Get a specific vehicle by vehicle_id
    """
    try:
        vehicle = db.query(Vehicle).filter(Vehicle.vehicle_id == vehicle_id).first()
        
        if not vehicle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vehicle {vehicle_id} not found"
            )
        
        return VehicleResponse(
            id=vehicle.id,
            vehicle_id=vehicle.vehicle_id,
            license_plate=vehicle.license_plate,
            vehicle_type=vehicle.vehicle_type,
            status=vehicle.status,
            driver_name=vehicle.driver_name,
            driver_phone=vehicle.driver_phone,
            created_at=vehicle.created_at,
            updated_at=vehicle.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving vehicle: {str(e)}"
        )

@router.put("/{vehicle_id}", response_model=VehicleResponse)
async def update_vehicle(
    vehicle_id: str,
    vehicle_data: VehicleUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a vehicle
    """
    try:
        vehicle = db.query(Vehicle).filter(Vehicle.vehicle_id == vehicle_id).first()
        
        if not vehicle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vehicle {vehicle_id} not found"
            )
        
        # Check license plate uniqueness if being updated
        if vehicle_data.license_plate and vehicle_data.license_plate != vehicle.license_plate:
            existing_plate = db.query(Vehicle).filter(
                Vehicle.license_plate == vehicle_data.license_plate,
                Vehicle.id != vehicle.id
            ).first()
            
            if existing_plate:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Vehicle with license plate {vehicle_data.license_plate} already exists"
                )
        
        # Update vehicle fields
        if vehicle_data.license_plate is not None:
            vehicle.license_plate = vehicle_data.license_plate
        if vehicle_data.vehicle_type is not None:
            vehicle.vehicle_type = vehicle_data.vehicle_type
        if vehicle_data.status is not None:
            vehicle.status = vehicle_data.status
        if vehicle_data.driver_name is not None:
            vehicle.driver_name = vehicle_data.driver_name
        if vehicle_data.driver_phone is not None:
            vehicle.driver_phone = vehicle_data.driver_phone
        
        vehicle.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(vehicle)
        
        return VehicleResponse(
            id=vehicle.id,
            vehicle_id=vehicle.vehicle_id,
            license_plate=vehicle.license_plate,
            vehicle_type=vehicle.vehicle_type,
            status=vehicle.status,
            driver_name=vehicle.driver_name,
            driver_phone=vehicle.driver_phone,
            created_at=vehicle.created_at,
            updated_at=vehicle.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating vehicle: {str(e)}"
        )

@router.delete("/{vehicle_id}", response_model=APIResponse)
async def delete_vehicle(
    vehicle_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a vehicle
    """
    try:
        vehicle = db.query(Vehicle).filter(Vehicle.vehicle_id == vehicle_id).first()
        
        if not vehicle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vehicle {vehicle_id} not found"
            )
        
        db.delete(vehicle)
        db.commit()
        
        return APIResponse(
            success=True,
            message=f"Vehicle {vehicle_id} deleted successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting vehicle: {str(e)}"
        )
