from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.security import InputValidator
from app.data_verifier import DataVerifier
from app.card_generator import ParkingCardGenerator
from datetime import datetime, timedelta
import hashlib
import os
from databases import Database
from sqlalchemy import create_engine
from app.models import Base, User, ParkingCard

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./parking.db")
database = Database(DATABASE_URL)

# Create sync engine for table creation
sync_db_url = DATABASE_URL.replace("+aiosqlite", "")  # Convert to sync SQLAlchemy URL
engine = create_engine(sync_db_url, connect_args={"check_same_thread": False})
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
cooldown_cache = {}

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

def get_data_hash(user_data: dict):
    data_str = f"{user_data['name']}{user_data['email']}{user_data['vehicle_reg']}"
    return hashlib.sha256(data_str.encode()).hexdigest()

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("generate_card.html", {"request": request})

@app.post("/generate-card")
async def generate_card(user_data: dict):
    InputValidator.validate_user_data(user_data)
    if not DataVerifier().verify_completion(user_data):
        return {"error": "Incomplete user data"}
    return ParkingCardGenerator().generate(user_data)
