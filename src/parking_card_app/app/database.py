from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException
from .models import Base, User, ParkingCard

class DatabaseHandler:
    def __init__(self, engine):
        self.engine = engine
        Base.metadata.create_all(bind=self.engine)
        
    def create_user_and_card(self, db: Session, user_data: dict, card_data: dict):
        """Atomically create/update user and card record"""
        try:
            # Check for existing user by email
            user = db.query(User).filter(User.email == user_data['email']).first()
            
            if user:
                # Verify vehicle ownership if updating registration
                if user.vehicle_reg != user_data['vehicle_reg']:
                    existing_vehicle = db.query(User).filter(
                        User.vehicle_reg == user_data['vehicle_reg']
                    ).first()
                    if existing_vehicle:
                        raise HTTPException(
                            status_code=400,
                            detail="Vehicle already registered to another user"
                        )
                    user.vehicle_reg = user_data['vehicle_reg']
                else:
                    # Allow renewals without changing vehicle_reg
                    pass  # No action needed for same vehicle registration
            else:
                # Create new user if doesn't exist
                user = User(
                    name=user_data['name'],
                    email=user_data['email'],
                    vehicle_reg=user_data['vehicle_reg']
                )
                db.add(user)
            
            db.flush()  # Get generated user ID
            
            # Create new card (allow multiple cards per user)
            card = ParkingCard(
                card_id=card_data['card_id'],
                user_id=user.id,
                expiry_date=datetime.strptime(card_data['expiry'], '%Y-%m-%d'),
                vehicle_reg=user_data['vehicle_reg']
            )
            db.add(card)
            db.commit()
            return user, card
        except Exception as e:
            db.rollback()
            raise
