from fastapi import HTTPException
import pytest
from app.card_generator import ParkingCardGenerator

def test_card_expiry():
    generator = ParkingCardGenerator()
    card = generator.generate({'vehicle_reg': 'ABC123'})
    assert 'expiry' in card
    assert len(card['card_id']) == 8
    assert card['card_id'].isalnum()

def test_invalid_generation():
    generator = ParkingCardGenerator()
    with pytest.raises(KeyError):
        generator.generate({})  # Missing required fields

def test_card_id_format():
    generator = ParkingCardGenerator()
    card = generator.generate({'vehicle_reg': 'TEST123'})
    assert len(card['card_id']) == 8
    assert all(c in '0123456789ABCDEF' for c in card['card_id'])

def test_unique_card_ids_for_same_vehicle():
    generator = ParkingCardGenerator()
    vehicle_reg = "SAME123"
    card1 = generator.generate({'vehicle_reg': vehicle_reg})
    card2 = generator.generate({'vehicle_reg': vehicle_reg})
    assert card1['card_id'] != card2['card_id'], "Card IDs should be unique even for same vehicle registration"
