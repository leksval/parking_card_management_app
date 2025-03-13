import os
import logging
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, joinedload
from app.models import ParkingCard, User

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("expiration_check.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("expiration_check")

def send_renewal_reminder(user_email, card_id, expiry_date):
    """Send expiration notice email directly without class"""
    msg = MIMEText(
        f"""Your parking card (ID: {card_id}) will expire on {expiry_date}.\n
        Please renew it within 30 days to avoid service interruption."""
    )
    msg['Subject'] = f'Parking Card Expiration Notice: {card_id}'
    msg['From'] = os.getenv("SMTP_USER", 'noreply@parkingsystem.com')
    msg['To'] = user_email
    
    try:
        with smtplib.SMTP(
            os.getenv("SMTP_SERVER", "smtp.example.com"), 
            int(os.getenv("SMTP_PORT", 587))
        ) as server:
            server.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASS"))
            server.send_message(msg)
    except Exception as e:
        logger.error(f"SMTP Error: {str(e)}")

def check_expiring_cards():
    """Check for cards expiring in the next 30 days and send notifications"""
    logger.info("Starting expiration check")
    
    # Database connection
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./parking.db")
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Find cards expiring in the next 30 days
        expiry_threshold = datetime.now() + timedelta(days=30)
        
        # Query cards with their associated users
        query = (
            select(ParkingCard, User)
            .join(User)
            .where(
                ParkingCard.expiry_date <= expiry_threshold,
                ParkingCard.expiry_date > datetime.now()
            )
        )
        
        expiring_cards = session.execute(query).all()
        logger.info(f"Found {len(expiring_cards)} cards expiring soon")
        
        # Send notifications
        for card, user in expiring_cards:
            try:
                send_renewal_reminder(
                    user_email=user.email,
                    card_id=card.card_id,
                    expiry_date=card.expiry_date.date().isoformat()
                )
                logger.info(f"Sent renewal notice to {user.email}")
            except Exception as e:
                logger.error(f"Failed to send notification to {user.email}: {str(e)}")
                
    except Exception as e:
        logger.error(f"Error checking expiring cards: {str(e)}")
    finally:
        session.close()
        
if __name__ == "__main__":
    check_expiring_cards()
