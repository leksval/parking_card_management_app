from sqlalchemy.orm import Session
from datetime import datetime
from .models import Base, User, ParkingCard

class DatabaseHandler:
    def __init__(self, engine):
        self.engine = engine
        Base.metadata.create_all(bind=self.engine)
        
    def create_user_and_card(self, db: Session, user_data: dict, card_data: dict):
        """Atomically create user and card record with proper transaction handling"""
        try:
            # Create and save user
            user = User(
                name=user_data['name'],
                email=user_data['email'],
                vehicle_reg=user_data['vehicle_reg']
            )
            db.add(user)
            db.flush()  # Get generated user ID
            
            # Create and save card
            card = ParkingCard(
                card_id=card_data['card_id'],
                user_id=user.id,
                expiry_date=datetime.strptime(card_data['expiry'], '%Y-%m-%d'),
                vehicle_reg=card_data['vehicle_reg']
            )
            db.add(card)
            db.commit()
            return user, card
        except Exception as e:
            db.rollback()
            raise
