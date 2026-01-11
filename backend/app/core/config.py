import os
from dotenv import load_dotenv

# Load .env file explicitly
load_dotenv()

class Settings:
    PROJECT_NAME: str = "LPR Backend"
    API_V1_STR: str = "/api/v1"
    
    # SECURITY
    SECRET_KEY: str = os.getenv("JWT_SECRET", "changethis_secret_key_please")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("JWT_EXPIRE_MINUTES", 120))
    
    # DATABASE
    # Defaults to local if not set in .env
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:password@127.0.0.1:5432/postgres")
    
    # EMAIL
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", 587))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    SMTP_FROM: str = os.getenv("SMTP_FROM", SMTP_USER)
    COMPLAINT_EMAIL_TO: str = os.getenv("COMPLAINT_EMAIL_TO", "admin@example.com")

settings = Settings()
