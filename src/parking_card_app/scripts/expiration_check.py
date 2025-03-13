import os
import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models import ParkingCard, User
from app.notifications import UserNotifier
from app.database import DatabaseHandler
from main import engine  # Reuse existing engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ExpirationCheck")

def check_expiring_cards():
    """Check for cards expiring within 30 days and send notifications"""
    db_handler = DatabaseHandler(engine)
    session = Session(engine)
    
    try:
        # Calculate threshold date
        threshold = datetime.utcnow() + timedelta(days=30)
        
        # Get expiring cards with user info
        expiring_cards = session.query(ParkingCard, User).join(
            User, ParkingCard.user_id == User.id
        ).filter(
            ParkingCard.expiry_date <= threshold,
            ParkingCard.expiry_date >= datetime.utcnow()
        ).all()

        notifier = UserNotifier(
            smtp_server=os.getenv("SMTP_SERVER"),
            port=int(os.getenv("SMTP_PORT", 587))
        )

        for card, user in expiring_cards:
            try:
                # Send email notification
                notifier.send_renewal_reminder(
                    user_email=user.email,
                    card_id=card.card_id,
                    expiry_date=card.expiry_date.date().isoformat()
                )
                logger.info(f"Sent renewal notice to {user.email} for card {card.card_id}")
            except Exception as e:
                logger.error(f"Failed to notify {user.email}: {str(e)}")

    except Exception as e:
        logger.error(f"Error checking expiring cards: {str(e)}")
    finally:
        session.close()

if __name__ == "__main__":
    check_expiring_cards()
