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
