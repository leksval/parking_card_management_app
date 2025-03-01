from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.security import InputValidator
from app.data_verifier import DataVerifier
from app.card_generator import ParkingCardGenerator

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("generate_card.html", {"request": request})

@app.post("/generate-card")
async def generate_card(user_data: dict):
    InputValidator.validate_user_data(user_data)
    if not DataVerifier().verify_completion(user_data):
        return {"error": "Incomplete user data"}
    return ParkingCardGenerator().generate(user_data)
