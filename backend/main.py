from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database import base, engine
import models.user
import models.swipe
import models.match
import models.images
from routes import auth, interactions, recommendations, profile, messages, images
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create database tables on startup
base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI(
    title="UCMe Matchmaking API",
    description="A college-specific dating app for UC students with endless scroll interface",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration - use explicit origins for security
# Default to localhost for development, can be overridden via environment
default_origins = [
    "http://localhost:3000",  # React dev server
    "http://localhost:3001",  # Alternative React port
    "http://127.0.0.1:3000", # Alternative localhost
    "http://127.0.0.1:3001", # Alternative localhost
]

# Get origins from environment or use defaults
cors_origins = os.getenv('CORS_ORIGINS', ','.join(default_origins)).split(',')
cors_origins = [origin.strip() for origin in cors_origins if origin.strip()]

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,  # Explicit origins instead of wildcard
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Explicit methods
    allow_headers=["*"],  # Keep headers flexible for auth tokens
)

# Include all API routers with proper prefixes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(interactions.router, prefix="/interactions", tags=["Interactions"])
app.include_router(recommendations.router, prefix="/recommendations", tags=["Recommendations"])
app.include_router(profile.router, prefix="/profile", tags=["Profile"])
app.include_router(messages.router, prefix="/messages", tags=["Messages"])
app.include_router(images.router, prefix="/images", tags=["Images"])

# Mount static files for serving uploaded images
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.get("/")
async def root():
    return {
        "message": "UCMe Matchmaking API",
        "status": "running",
        "version": "1.0.0",
        "features": [
            "UC email verification",
            "JWT authentication", 
            "Like/Pass interactions",
            "Match creation",
            "Endless scroll recommendations",
            "Profile management"
        ]
    }

