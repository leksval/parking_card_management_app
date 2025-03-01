from src.parking_card_app.app.card_generator import ParkingCardGenerator

def test_card_expiry():
    generator = ParkingCardGenerator()
    card = generator.generate({'vehicle_reg': 'ABC123'})
    assert 'expiry' in card
    assert len(card['card_id']) == 36
