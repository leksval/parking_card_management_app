# Parking Management System API 
A modern parking permit management system with automated card generation and user validation.

## Features ✨
- **Multi-Card Support** - Generate multiple permits per vehicle/user
- **Ownership Verification** - Strict vehicle registration checks
- **Renewal System** - Generate new cards with updated expiration
- **Expiration Notifications** - Automated email reminders for expiring cards
- **Validation Pipeline**:
  - Input sanitization
  - Email format validation (RFC 5322)
  - Vehicle registration pattern matching
  - SMTP email notifications
  - Database integrity checks
- **Transaction Safety** - Atomic database operations
- **Audit Trail** - Full card generation history

## Installation ⚙️
 

### Prerequisites
- Python 3.9+
- Docker

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

### Core Endpoints
### Generate Parking Permit
`POST /generate-card` - Create new parking card with email confirmation
```http
POST /check-registration
```

**Request Body:**
```json
{
    "name": "John Doe",
    "email": "john@example.com",
    "vehicle_reg": "ABC123"
}
```

**Response:**
```json
{
    "exists": true,
    "is_owner": false
}
```

### Registration Check
`POST /check-registration` - Verify vehicle ownership status

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

## Environment Variables ⚙️
Create `.env` file:
```ini
# Production
SMTP_SERVER=smtp.example.com
SMTP_PORT=587
SMTP_USER=your_email@example.com
SMTP_PASS=your_email_password
DATABASE_URL=sqlite+aiosqlite:////app/data/parking.db

# Development
DEBUG=true
```

## Architecture 🛠️
| Component            | Technology           |
|----------------------|----------------------| 
| Backend Framework    | FastAPI              |
| Database             | SQLite + SQLAlchemy  |
| Async Database       | Databases + aiosqlite|
| Input Validation     | Regex + Custom Rules |
| Testing              | pytest               |
| Frontend             | Jinja2 Templates     |
| Styling              | Tailwind CSS 3       |

### Project Structure
```
parking_card_app/
├── app/
│   ├── __init__.py
│   ├── card_generator.py  # Permit generation logic
│   ├── data_verifier.py   # Cross-system data checks
│   ├── database.py       # Atomic transaction handler
│   ├── security.py       # Validation pipeline
│   ├── card_generator.py # UUID-based ID generation
│   └── models.py         # Database schema definitions
├── scripts/
│   ├── expiration_check.py # Card expiration checker
│   └── start.sh           # Container startup script
├── static/
│   └── css/style.css     # Animation/UI enhancements
├── templates/             # UI components
├── tests/                 # Test cases
├── Dockerfile
├── main.py                # Entry point
└── requirements.txt
```

## Development 🤝
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
