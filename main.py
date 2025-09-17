from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import logging
import uvicorn

from config.settings import settings
from database.database import init_db, test_db_connection
from api.gps_api import router as gps_router
from api.vehicle_api import router as vehicle_router
from api.area_api import router as area_router
from api.dashboard_api import router as dashboard_router

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(settings.log_file),
        logging.StreamHandler()
    ]
)

# Create FastAPI app
app = FastAPI(
    title="GPS Area Tracking System",
    description="Real-time GPS tracking system with area management",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Include API routers
app.include_router(gps_router)
app.include_router(vehicle_router)
app.include_router(area_router)
app.include_router(dashboard_router)

@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    logging.info("Starting GPS Area Tracking System...")
    
    # Test database connection
    if test_db_connection():
        logging.info("Database connection successful")
        # Initialize database tables
        init_db()
        logging.info("Database initialized")
    else:
        logging.error("Database connection failed")
        raise Exception("Cannot start application without database connection")

@app.get("/")
async def root(request: Request):
    """Serve the main map page"""
    return templates.TemplateResponse("map.html", {"request": request})

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "GPS Area Tracking System is running",
        "version": "1.0.0"
    }

@app.get("/api/status")
async def api_status():
    """API status endpoint"""
    return {
        "api_version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "gps": "/api/gps",
            "vehicles": "/api/vehicles",
            "areas": "/api/areas",
            "dashboard": "/api/dashboard"
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_debug,
        log_level=settings.log_level.lower()
    )
