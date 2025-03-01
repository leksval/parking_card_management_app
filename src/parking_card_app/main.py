from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.security import InputValidator
from app.data_verifier import DataVerifier
from app.card_generator import ParkingCardGenerator
from datetime import datetime, timedelta
import hashlib

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
cooldown_cache = {}

def get_data_hash(user_ dict):
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
