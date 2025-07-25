# SQLAlchemy DB connection and session 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import os
from dotenv import load_dotenv

load_dotenv()
databaseUrl = os.getenv('dburl')
if not databaseUrl:
    raise RuntimeError("Failed to retrieve database from .env file")

engine = create_engine(databaseUrl) #Create database engine
localSession = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
base = declarative_base()

def get_db():
    db = localSession() #Create a new session for the database
    try:
        yield db
    finally:
        db.close()