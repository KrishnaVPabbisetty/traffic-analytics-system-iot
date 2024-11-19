from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routes import traffic
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def create_application() -> FastAPI:
    """Create and configure the FastAPI application"""

    # Initialize FastAPI app
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
        description="Traffic Analytics System API",
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],  # React frontend URL
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(traffic.router, tags=["Traffic"])

    return app


# Create the FastAPI application
app = create_application()


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint to check API status"""
    return {
        "status": "online",
        "service": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
    }


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    logger.error(f"HTTP error occurred: {exc.detail}")
    return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    logger.error(f"Unexpected error occurred: {str(exc)}")
    return JSONResponse(status_code=500, content={"message": "Internal server error"})


# Startup event
@app.on_event("startup")
async def startup_event():
    """Execute actions on application startup"""
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.PROJECT_VERSION}")
    # You can add initialization code here (e.g., database connections)


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Execute actions on application shutdown"""
    logger.info(f"Shutting down {settings.PROJECT_NAME}")
    # You can add cleanup code here


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
