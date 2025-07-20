# SQLAlchemy DB connection and session 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()
databaseUrl = os.getenv('dburl')
if not databaseUrl:
    raise RuntimeError("Failed to retrieve database from .env file")

engine = create_engine(databaseUrl)
localSession = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
base = declarative_base()
