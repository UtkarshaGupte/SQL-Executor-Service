from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import models
from typing import List, Annotated
from db.database import engine, SessionLocal
from sqlalchemy.orm import Session
from routes import problems
from db.database import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(problems.router)