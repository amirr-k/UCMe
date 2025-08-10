# SQLAlchemy DB connection and session 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import os
from dotenv import load_dotenv

load_dotenv()

# Use DATABASE_URL instead of dburl for consistency
databaseUrl = os.getenv('DATABASE_URL')
if not databaseUrl:
    raise RuntimeError("DATABASE_URL not found in environment variables. Please check your .env file")

# Ensure we're using PostgreSQL (required for ARRAY columns)
if not databaseUrl.startswith('postgresql://'):
    raise RuntimeError("DATABASE_URL must point to a PostgreSQL database. ARRAY columns are not supported in SQLite.")

# Convert to asyncpg dialect for better macOS compatibility
if databaseUrl.startswith('postgresql://'):
    databaseUrl = databaseUrl.replace('postgresql://', 'postgresql+asyncpg://', 1)

engine = create_engine(databaseUrl) #Create database engine
localSession = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
base = declarative_base()

def get_db():
    db = localSession() #Create a new session for the database
    try:
        yield db
    finally:
        db.close()