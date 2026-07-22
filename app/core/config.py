import os
from pathlib import Path
from dotenv import load_dotenv
import logging
import sys

# Load .env from project root
env_path = Path(__file__).absolute().parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path, override=True)

class Settings:
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Contact API")
    PROJECT_VERSION: str = os.getenv("PROJECT_VERSION", "1.0.0")
    API_PREFIX: str = os.getenv("API_PREFIX", "/api")
    
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test_task.db")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME: str = os.getenv("SMTP_USERNAME", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    SMTP_FROM_EMAIL: str = os.getenv("SMTP_FROM_EMAIL", "")
    
    RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", "10"))
    RATE_LIMIT_WINDOW: int = int(os.getenv("RATE_LIMIT_WINDOW", "60"))
    
    CORS_ORIGINS: list = [origin.strip() for origin in os.getenv("CORS_ORIGINS", "*").split(",") if origin.strip()]

settings = Settings()

def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG if settings.DEBUG else logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('app.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
