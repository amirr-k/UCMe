from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import base, engine
import models.user
import models.swipe
import models.match
import models.images
from routes import auth, interactions, recommendations, profile, messages

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

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all API routers with proper prefixes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(interactions.router, prefix="/interactions", tags=["Interactions"])
app.include_router(recommendations.router, prefix="/recommendations", tags=["Recommendations"])
app.include_router(profile.router, prefix="/profile", tags=["Profile"])
app.include_router(messages.router, prefix="/messages", tags=["Messages"])


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

