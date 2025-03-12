from fastapi import HTTPException
import pytest
from app.card_generator import ParkingCardGenerator

def test_card_expiry():
    generator = ParkingCardGenerator()
    card = generator.generate({'vehicle_reg': 'ABC123'})
    assert 'expiry' in card
    assert len(card['card_id']) == 36

def test_invalid_generation():
    generator = ParkingCardGenerator()
    with pytest.raises(KeyError):
        generator.generate({})  # Missing required fields
