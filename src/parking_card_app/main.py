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
from sqlalchemy.orm import sessionmaker
from app.models import Base, User, ParkingCard
from app.database import DatabaseHandler

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./parking.db")
database = Database(DATABASE_URL)

# Create sync engine for table creation
sync_db_url = DATABASE_URL.replace("+aiosqlite", "")  # Convert to sync SQLAlchemy URL
engine = create_engine(sync_db_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
cooldown_cache = {}
app.db_handler = DatabaseHandler(engine)

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

@app.post("/check-registration")
async def check_registration(vehicle_data: dict):
    db = SessionLocal()
    try:
        existing = db.query(User).filter(
            User.vehicle_reg == vehicle_data['vehicle_reg']
        ).first()
        
        if existing:
            return {
                "exists": True,
                "is_owner": existing.email == vehicle_data.get('email', '')
            }
        return {"exists": False}
    finally:
        db.close()

@app.post("/generate-card")
async def generate_card(user_data: dict):
    await InputValidator.validate_user_data(user_data)
    if not DataVerifier().verify_completion(user_data):
        raise HTTPException(status_code=400, detail="Incomplete user data")
    
    db = SessionLocal()
    try:
        # Generate card data
        generator = ParkingCardGenerator()
        card_data = generator.generate(user_data)
        
        # Save to database
        user, card = app.db_handler.create_user_and_card(db, user_data, card_data)
        
        return {
            "card_id": card_data['card_id'],
            "vehicle_reg": card_data['vehicle_reg'],
            "expiry": card_data['expiry'],
            "created_at": card.created_at.isoformat(),
            "database_id": card.id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database error") from e
    finally:
        db.close()
