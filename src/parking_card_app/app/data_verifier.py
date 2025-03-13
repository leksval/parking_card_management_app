class DataVerifier:
    REQUIRED_FIELDS = ['name', 'email', 'vehicle_reg']
    
    def verify_completion(self, user_data):
        return all(user_data.get(field) for field in self.REQUIRED_FIELDS)
        
    async def check_existing_registration(self, vehicle_reg: str):
        from main import database  # Import inside method to avoid circular imports
        from app.models import User
        query = User.__table__.select().where(User.vehicle_reg == vehicle_reg)
        existing = await database.fetch_one(query)
        return existing is not None
        
    async def check_existing_email(self, email: str):
        from main import database
        from app.models import User
        query = User.__table__.select().where(User.email == email)
        return await database.fetch_one(query) is not None

    async def check_vehicle_owner(self, email: str, vehicle_reg: str):
        from main import database
        from app.models import User
        query = User.__table__.select().where(
            (User.email == email) & 
            (User.vehicle_reg != vehicle_reg)
        )
        return await database.fetch_one(query) is not None
        
    async def is_vehicle_owned_by_another_user(self, vehicle_reg: str, email: str):
        from main import database
        from app.models import User
        query = User.__table__.select().where(
            (User.vehicle_reg == vehicle_reg) &
            (User.email != email)
        )
        return await database.fetch_one(query) is not None
