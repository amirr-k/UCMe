# SQLAlchemy DB connection and session 
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
databaseUrl = os.getenv('dburl')

engine = create_engine(databaseUrl)
localSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
base = declarative_base()

