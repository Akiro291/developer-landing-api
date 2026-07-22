# Contact API Backend Service

## Overview
REST API service for handling contact form submissions with AI analysis and email notifications.

## Tech Stack
- Python 3.11
- FastAPI
- SQLAlchemy
- SQLite
- Google Gemini API
- SMTP Gmail
- Vue.js 3
- Vite
- Docker

## Project Structure
```
test-task/
├── app/                  # Backend application
│   ├── api/              # API endpoints
│   ├── core/             # Core configuration and utilities
│   ├── models/           # Database models
│   ├── schemas/          # Pydantic schemas
│   ├── services/         # Business logic services
│   ├── database/         # Database connection
│   ├── utils/            # Utility functions
│   ├── main.py           # Application entry point
│   └── __init__.py
├── frontend/             # Vue.js frontend
│   ├── src/
│   │   ├── components/
│   │   ├── assets/
│   │   ├── App.vue
│   │   └── main.js
│   ├── public/
│   ├── index.html
│   └── vite.config.js
├── tests/                # Unit tests
├── storage/              # Storage for rate limits and metrics
├── static/               # Static files
├── requirements.txt      # Python dependencies
├── requirements-dev.txt  # Development dependencies
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

## Features
- Contact form submission with validation
- AI-powered comment analysis using Google Gemini API
- Email notifications via SMTP
- Rate limiting protection
- Global exception handling
- CORS support
- Comprehensive logging
- Swagger documentation
- Vue.js 3 frontend with Vite
- Docker support for easy deployment

## Setup

### Prerequisites
- Python 3.11+
- Node.js 18+ (for frontend)
- Docker & Docker Compose (optional)

### Local Development

#### Backend
```bash
# Clone the repository
git clone <repository-url>
cd test-task

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from template
cp .env.example .env
# Edit .env with your configuration

# Run the application
uvicorn app.main:app --reload
```

#### Frontend
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

### Docker
```bash
# Build and run with Docker Compose
docker-compose up --build

# Or run with Docker directly
docker build -t contact-api .
docker run -p 8000:8000 contact-api
```

## Environment Variables
Copy `.env.example` to `.env` and configure:

### Backend
- `DATABASE_URL` - Database connection string (default: SQLite)
- `DEBUG` - Debug mode (default: False)
- `GEMINI_API_KEY` - Google Gemini API key
- `SMTP_HOST`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_PASSWORD` - SMTP configuration
- `SMTP_FROM_EMAIL` - Sender email address
- `RATE_LIMIT_REQUESTS`, `RATE_LIMIT_WINDOW` - Rate limiting settings
- `CORS_ORIGINS` - Allowed CORS origins

### Frontend
- `VITE_API_URL` - Backend API URL (default: http://localhost:8000)

## API Endpoints
- `POST /api/contact` - Submit contact form
- `GET /api/system/health` - Health check
- `GET /` - Root endpoint
- `/docs` - Swagger UI
- `/redoc` - ReDoc documentation

## AI Integration
The backend uses Google Gemini API to analyze contact form comments for sentiment, spam detection, and key insights.

### Architecture
```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Frontend  │────▶│   Backend    │────▶│  Google     │
│  (Vue.js)   │     │  (FastAPI)   │     │  Gemini API │
└─────────────┘     └──────────────┘     └─────────────┘
                         │
                         ▼
                  ┌─────────────┐
                  │   SMTP      │
                  │   Gmail     │
                  └─────────────┘
```

## Examples

### Request Example
```bash
curl -X POST http://localhost:8000/api/contact \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "message": "I have a question about your services"
  }'
```

### Response Example
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "message": "I have a question about your services",
  "analyzed": true,
  "sentiment": "neutral",
  "is_spam": false,
  "created_at": "2026-07-22T21:34:29+05:00"
}
```

## Testing
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/ -v
```

## Deployment
See [DOCKER_README.md](DOCKER_README.md) for Docker deployment details.

## License
MIT
