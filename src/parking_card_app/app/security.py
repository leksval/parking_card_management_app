from fastapi import HTTPException
import re
from app.data_verifier import DataVerifier

class InputValidator:
    @staticmethod
    async def validate_user_data(data):
        """
        Performs comprehensive input validation:
        1. Checks for required fields
        2. Validates email format using RFC 5322 pattern
        3. Ensures vehicle registration matches agency format
        4. Verifies vehicle ownership through database
        
        Raises:
            HTTPException: For any validation failures
        """
        required = ['name', 'email', 'vehicle_reg']
        if not all(field in data for field in required):
            raise HTTPException(status_code=400, detail="Missing required fields")
        
        # Trim and validate each field
        name = data['name'].strip()
        email = data['email'].strip()
        vehicle_reg = data['vehicle_reg'].strip().upper()

        if not name or len(name) < 2:
            raise HTTPException(status_code=400, detail="Name must be at least 2 characters")
            
        # Regex explanation: Simplified RFC 5322 email pattern
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            raise HTTPException(status_code=400, detail="Invalid email format")

        if not re.match(r'^[A-Z0-9]{5,8}$', vehicle_reg):
            raise HTTPException(status_code=400, detail="Vehicle registration must be 5-8 alphanumeric characters")
        
        # Add new database check
        verifier = DataVerifier()
        if await verifier.is_vehicle_owned_by_another_user(vehicle_reg, email):
            raise HTTPException(status_code=400, detail="Vehicle already registered to another user")
        
        # Add email existence check
        if await verifier.check_existing_email(email):
            if await verifier.check_vehicle_owner(email, vehicle_reg):
                raise HTTPException(400, "Vehicle already registered to another email")
        
        # Update data with cleaned values
        data.update({
            'name': name,
            'email': email,
            'vehicle_reg': vehicle_reg
        })
