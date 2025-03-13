import uuid
from datetime import datetime, timedelta

class ParkingCardGenerator:
    def generate(self, user_data):
        """
        Generates a new parking card with:
        - 8-character uppercase UUID
        - 1-year expiration from generation
        - Linked vehicle registration
        
        Returns: Dict with card_id, expiry, vehicle_reg
        """
        # UUID provides collision resistance while being readable
        return {
            'card_id': str(uuid.uuid4().hex[:8]).upper(),
            # Standard 1-year validity period
            'expiry': (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d'),
            'vehicle_reg': user_data['vehicle_reg']
        }
