from fastapi import HTTPException

class InputValidator:
    @staticmethod
    def validate_user_data(data):
        required = ['name', 'email', 'vehicle_reg']
        if not all(field in data for field in required):
            raise HTTPException(status_code=400, detail="Missing required fields")
