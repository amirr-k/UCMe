from fastapi import FastAPI
from database import base, engine
import models.user


Base.metadata.create_all(bind=engine)
app = FastAPI()