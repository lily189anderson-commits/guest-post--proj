"""
Centralized configuration. All environment-dependent values are read here
and nowhere else, so the rest of the app never touches os.environ directly.
"""
import os
from dataclasses import dataclass

# Loads a local .env file if python-dotenv is installed (optional convenience)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


@dataclass
class Settings:
    # Example Postgres URL:
    #   postgresql+psycopg2://gp_user:gp_password@localhost:5432/guest_post_engine
    # Falls back to a local SQLite file if not set, so `uvicorn` runs out of the box.
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./guest_post_engine.db")

    SECRET_KEY: str = os.getenv("SECRET_KEY", "CHANGE_THIS_SECRET_KEY_IN_PRODUCTION")
    ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "480"))

    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "*")

    DEFAULT_ADMIN_USERNAME: str = os.getenv("DEFAULT_ADMIN_USERNAME", "admin")
    DEFAULT_ADMIN_PASSWORD: str = os.getenv("DEFAULT_ADMIN_PASSWORD", "admin123")


settings = Settings()
