"""
Database engine & session factory.

Reads DATABASE_URL from environment/config. Designed for PostgreSQL in
production (see .env.example), and falls back to a local SQLite file if
no DATABASE_URL is set, so the project can be run immediately without
installing Postgres first.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.infrastructure.database.base import Base

connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    """Create all tables. In production, prefer Alembic migrations instead."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """FastAPI dependency: yields a DB session per-request, always closed after."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
