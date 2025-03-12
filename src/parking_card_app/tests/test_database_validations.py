import pytest
from datetime import datetime
from fastapi import HTTPException
from app.models import User, ParkingCard, Base
from app.data_verifier import DataVerifier
from app.security import InputValidator
from databases import Database
from sqlalchemy import create_engine

@pytest.fixture(scope="module")
def test_db():
    # Use in-memory SQLite for testing
    DATABASE_URL = "sqlite+aiosqlite:///:memory:"
    engine = create_engine(DATABASE_URL.replace("+aiosqlite", ""))
    Base.metadata.create_all(engine)
    database = Database(DATABASE_URL)
    return database

@pytest.mark.asyncio
async def test_database_connection(test_db):
    await test_db.connect()
    assert test_db.is_connected
    await test_db.disconnect()

@pytest.mark.asyncio
async def test_user_creation(test_db):
    await test_db.connect()
    
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "vehicle_reg": "TEST123"
    }
    
    # Insert new user
    insert_query = User.__table__.insert().values(**user_data)
    user_id = await test_db.execute(insert_query)
    
    # Retrieve user
    select_query = User.__table__.select().where(User.id == user_id)
    user = await test_db.fetch_one(select_query)
    
    assert user is not None
    assert user["email"] == "test@example.com"
    await test_db.disconnect()

@pytest.mark.asyncio
async def test_duplicate_vehicle_registration(test_db):
    await test_db.connect()
    verifier = DataVerifier()
    
    # First registration
    await test_db.execute(
        User.__table__.insert().values(
            name="First User",
            email="first@example.com",
            vehicle_reg="DUPE123"
        )
    )
    
    # Test duplicate detection
    with pytest.raises(HTTPException) as exc:
        await InputValidator.validate_user_data({
            "name": "Second User",
            "email": "second@example.com",
            "vehicle_reg": "DUPE123"
        })
        
    assert exc.value.status_code == 400
    assert "Vehicle already registered" in str(exc.value.detail)
    await test_db.disconnect()

@pytest.mark.asyncio
async def test_email_validation(test_db):
    await test_db.connect()
    
    invalid_emails = [
        "missing@domain",
        "noatsign.com",
        "invalid@.com",
        "@missingusername.com"
    ]
    
    for email in invalid_emails:
        with pytest.raises(HTTPException) as exc:
            await InputValidator.validate_user_data({
                "name": "Test User",
                "email": email,
                "vehicle_reg": "TEST123"
            })
        assert "Invalid email format" in str(exc.value.detail)
    
    await test_db.disconnect()

@pytest.mark.asyncio
async def test_multiple_cards_per_user(test_db):
    await test_db.connect()
    
    # Create user
    user_id = await test_db.execute(
        User.__table__.insert().values(
            name="Multi Card User",
            email="multi@example.com",
            vehicle_reg="MULTI123"
        )
    )
    
    # Generate two cards
    card1 = ParkingCard.__table__.insert().values(
        card_id="CARD-001",
        user_id=user_id,
        expiry_date=datetime.now()
    )
    
    card2 = ParkingCard.__table__.insert().values(
        card_id="CARD-002",
        user_id=user_id,
        expiry_date=datetime.now()
    )
    
    await test_db.execute(card1)
    await test_db.execute(card2)
    
    # Verify card count
    query = ParkingCard.__table__.select().where(ParkingCard.user_id == user_id)
    cards = await test_db.fetch_all(query)
    
    assert len(cards) == 2
    await test_db.disconnect()
