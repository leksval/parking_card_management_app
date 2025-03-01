import uuid
from datetime import datetime, timedelta

class ParkingCardGenerator:
    def generate(self, user_data):
        return {
            'card_id': str(uuid.uuid4()),
            'vehicle_reg': user_data['vehicle_reg'],
            'expiry': (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d')
        }
