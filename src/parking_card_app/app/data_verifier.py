class DataVerifier:
    REQUIRED_FIELDS = ['name', 'email', 'vehicle_reg', 'contact']
    
    def verify_completion(self, user_data):
        return all(user_data.get(field) for field in self.REQUIRED_FIELDS)
