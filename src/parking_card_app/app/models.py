from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    vehicle_reg = Column(String(20), unique=True, nullable=False)
    cards = relationship("ParkingCard", back_populates="user")

class ParkingCard(Base):
    __tablename__ = "parking_cards"
    id = Column(Integer, primary_key=True, index=True)
    card_id = Column(String(8), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    expiry_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    vehicle_reg = Column(String(20), nullable=False)
    user = relationship("User", back_populates="cards")
    
    __table_args__ = (
        Index('ix_expiry_date', 'expiry_date'),
        Index('ix_vehicle_reg', 'vehicle_reg'),
    )
