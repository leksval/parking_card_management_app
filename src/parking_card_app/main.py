from fastapi import FastAPI
from app.security import InputValidator
from app.data_verifier import DataVerifier
from app.card_generator import ParkingCardGenerator

app = FastAPI()

@app.post("/generate-card")
async def generate_card(user_data: dict):
    InputValidator.validate_user_data(user_data)
    if not DataVerifier().verify_completion(user_data):
        return {"error": "Incomplete user data"}
    return ParkingCardGenerator().generate(user_data)
