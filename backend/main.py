from fastapi import FastAPI
from database import base, engine
import models.user
from routes import register, auth

# Create database tables
base.metadata.create_all(bind=engine)

app = FastAPI(
    title="UCMe Matchmaking API",
    description="A college-specific dating app for UC students",
    version="1.0.0"
)
app.include_router(register.router, prefix="/auth", tags=["auth"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])

