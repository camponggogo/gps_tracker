from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from database.database import get_db
from database.models import Area, AreaType, AreaShape
from api.schemas import (
    AreaCreate, AreaUpdate, AreaResponse, 
    APIResponse, PaginatedResponse
)

router = APIRouter(prefix="/api/areas", tags=["Areas"])

@router.post("/", response_model=AreaResponse)
async def create_area(
    area_data: AreaCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new area (entrance, alert, critical, checkpoint)
    """
    try:
        # Validate coordinates based on shape
        if not validate_coordinates(area_data.coordinates, area_data.shape):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid coordinates for {area_data.shape.value} shape"
            )
        
        # Create new area
        area = Area(
            name=area_data.name,
            area_type=area_data.area_type,
            shape=area_data.shape,
            coordinates=area_data.coordinates,
            buffer_distance=area_data.buffer_distance or 0.0,
            is_active=True
        )
        
        db.add(area)
        db.commit()
        db.refresh(area)
        
        return AreaResponse(
            id=area.id,
            name=area.name,
            area_type=area.area_type,
            shape=area.shape,
            coordinates=area.coordinates,
            buffer_distance=area.buffer_distance,
            is_active=area.is_active,
            created_at=area.created_at,
            updated_at=area.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating area: {str(e)}"
        )

@router.get("/", response_model=PaginatedResponse)
async def get_areas(
    db: Session = Depends(get_db),
    area_type: Optional[AreaType] = None,
    shape: Optional[AreaShape] = None,
    is_active: Optional[bool] = None,
    page: int = 1,
    size: int = 50
):
    """
    Get list of areas with optional filtering
    """
    try:
        # Build query
        query = db.query(Area)
        
        if area_type:
            query = query.filter(Area.area_type == area_type)
        
        if shape:
            query = query.filter(Area.shape == shape)
        
        if is_active is not None:
            query = query.filter(Area.is_active == is_active)
        
        # Get total count
        total = query.count()
        
        # Get paginated results
        areas = query.order_by(Area.created_at.desc()).offset(
            (page - 1) * size
        ).limit(size).all()
        
        # Convert to response format
        items = []
        for area in areas:
            items.append(AreaResponse(
                id=area.id,
                name=area.name,
                area_type=area.area_type,
                shape=area.shape,
                coordinates=area.coordinates,
                buffer_distance=area.buffer_distance,
                is_active=area.is_active,
                created_at=area.created_at,
                updated_at=area.updated_at
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
            detail=f"Error retrieving areas: {str(e)}"
        )

@router.get("/{area_id}", response_model=AreaResponse)
async def get_area(
    area_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific area by ID
    """
    try:
        area = db.query(Area).filter(Area.id == area_id).first()
        
        if not area:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Area {area_id} not found"
            )
        
        return AreaResponse(
            id=area.id,
            name=area.name,
            area_type=area.area_type,
            shape=area.shape,
            coordinates=area.coordinates,
            buffer_distance=area.buffer_distance,
            is_active=area.is_active,
            created_at=area.created_at,
            updated_at=area.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving area: {str(e)}"
        )

@router.put("/{area_id}", response_model=AreaResponse)
async def update_area(
    area_id: int,
    area_data: AreaUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an area
    """
    try:
        area = db.query(Area).filter(Area.id == area_id).first()
        
        if not area:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Area {area_id} not found"
            )
        
        # Validate coordinates if being updated
        if area_data.coordinates and area_data.shape:
            if not validate_coordinates(area_data.coordinates, area_data.shape):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid coordinates for {area_data.shape.value} shape"
                )
        
        # Update area fields
        if area_data.name is not None:
            area.name = area_data.name
        if area_data.area_type is not None:
            area.area_type = area_data.area_type
        if area_data.shape is not None:
            area.shape = area_data.shape
        if area_data.coordinates is not None:
            area.coordinates = area_data.coordinates
        if area_data.buffer_distance is not None:
            area.buffer_distance = area_data.buffer_distance
        if area_data.is_active is not None:
            area.is_active = area_data.is_active
        
        area.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(area)
        
        return AreaResponse(
            id=area.id,
            name=area.name,
            area_type=area.area_type,
            shape=area.shape,
            coordinates=area.coordinates,
            buffer_distance=area.buffer_distance,
            is_active=area.is_active,
            created_at=area.created_at,
            updated_at=area.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating area: {str(e)}"
        )

@router.delete("/{area_id}", response_model=APIResponse)
async def delete_area(
    area_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete an area
    """
    try:
        area = db.query(Area).filter(Area.id == area_id).first()
        
        if not area:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Area {area_id} not found"
            )
        
        db.delete(area)
        db.commit()
        
        return APIResponse(
            success=True,
            message=f"Area {area_id} deleted successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting area: {str(e)}"
        )

@router.get("/types/{area_type}", response_model=List[AreaResponse])
async def get_areas_by_type(
    area_type: AreaType,
    db: Session = Depends(get_db),
    is_active: Optional[bool] = True
):
    """
    Get all areas of a specific type
    """
    try:
        query = db.query(Area).filter(Area.area_type == area_type)
        
        if is_active is not None:
            query = query.filter(Area.is_active == is_active)
        
        areas = query.order_by(Area.name).all()
        
        items = []
        for area in areas:
            items.append(AreaResponse(
                id=area.id,
                name=area.name,
                area_type=area.area_type,
                shape=area.shape,
                coordinates=area.coordinates,
                buffer_distance=area.buffer_distance,
                is_active=area.is_active,
                created_at=area.created_at,
                updated_at=area.updated_at
            ))
        
        return items
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving areas by type: {str(e)}"
        )

def validate_coordinates(coordinates: dict, shape: AreaShape) -> bool:
    """
    Validate coordinates based on area shape
    """
    try:
        if shape == AreaShape.CIRCLE:
            # Circle should have center and radius
            center = coordinates.get("center", {})
            radius = coordinates.get("radius", 0)
            
            if not center.get("lat") or not center.get("lng"):
                return False
            
            if radius <= 0:
                return False
        
        elif shape == AreaShape.RECTANGLE:
            # Rectangle should have bounds
            bounds = coordinates.get("bounds", {})
            
            required_keys = ["north", "south", "east", "west"]
            if not all(key in bounds for key in required_keys):
                return False
            
            # Check if bounds are valid
            if bounds["north"] <= bounds["south"]:
                return False
            
            if bounds["east"] <= bounds["west"]:
                return False
        
        elif shape == AreaShape.POLYGON:
            # Polygon should have points array
            points = coordinates.get("points", [])
            
            if len(points) < 3:
                return False
            
            # Check if each point has lat and lng
            for point in points:
                if not point.get("lat") or not point.get("lng"):
                    return False
        
        return True
        
    except Exception:
        return False
