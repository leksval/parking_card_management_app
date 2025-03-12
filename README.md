# Parking Management System API 
A modern parking permit management system with automated card generation and user validation.

## Features ✨
- **Secure Data Validation** - Strict input validation for user information
- **Preview System** - Confirm details before final submission
- **Docker Support** - Easy containerized deployment
- **Responsive UI** - Clean, modern interface with Tailwind CSS

https://github.com/user-attachments/assets/75692bb9-ae5f-4254-9f56-88e442dc97b3

## Installation ⚙️

### Prerequisites
- Python 3.9+
- Docker (optional)

### Quick Start with Docker
```bash
# Build and run
docker build -t parking-app . && docker run -p 8000:8000 parking-app

# Access the app
open http://localhost:8000
```

### Manual Setup
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## API Reference 📚

### Generate Parking Permit
```http
POST /generate-card
```

**Request Body:**
```json
{
    "name": "John Doe",
    "email": "john@example.com",
    "vehicle_reg": "ABC123"
}
```

**Success Response:**
```json
{
    "card_id": "550e8400-e29b-41d4-a716-446655440000",
    "vehicle_reg": "ABC123", 
    "expiry": "2025-03-20"
}
```

**Error Responses:**
- `400 Bad Request` - Invalid input data
- `429 Too Many Requests` - Rate limit exceeded

**Example CURL:**
```bash
curl -X POST "http://localhost:8000/generate-card" \
     -H "Content-Type: application/json" \
     -d '{"name":"John","email":"john@test.com","vehicle_reg":"ABC123"}'
```

## Configuration ⚙️
Create `.env` file:
```ini
# Production
SMTP_SERVER=smtp.example.com
SMTP_PORT=587
SMTP_USER=admin@parking.com
SMTP_PASS=securepassword

# Development
DEBUG=true
```

## Tech Stack 🛠️
| Component            | Technology           |
|----------------------|----------------------|
| Backend Framework    | FastAPI              |
| Templating           | Jinja2               |
| Styling              | Tailwind CSS         |
| Containerization     | Docker               |
| Validation           | Pydantic (implied)   |
| Testing              | pytest               |

### Project Structure
```
parking_card_app/
├── app/
│   ├── __init__.py
│   ├── card_generator.py  # Permit generation logic
│   ├── data_verifier.py   # Data completeness checks
│   ├── notifications.py   # Email reminders
│   └── security.py        # Validation & sanitization
├── static/
│   └── css/style.css      # Custom styles
├── templates/             # UI components
├── tests/                 # Test cases
├── Dockerfile
├── main.py                # Entry point
└── requirements.txt
```

## Contributing 🤝
1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-validator`
3. Commit changes: `git commit -m 'Add validation pattern'`
4. Push branch: `git push origin feature/new-validator`
5. Open pull request

### Development Setup
```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest -v tests/
```
