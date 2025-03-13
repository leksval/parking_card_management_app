import uuid
from datetime import datetime, timedelta

class ParkingCardGenerator:
    def generate(self, user_data, expiry_days=365):  # Add expiry_days parameter
        return {
            'card_id': str(uuid.uuid4().hex[:8]).upper(),
            'vehicle_reg': user_data['vehicle_reg'],
            'expiry': (datetime.now() + timedelta(days=expiry_days)).strftime('%Y-%m-%d')
        }
