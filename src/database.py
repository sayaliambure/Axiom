"""
Database configuration and session management for AXIOM.

Uses SQLAlchemy for ORM and PostgreSQL as the database.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database
    database_url: str = "postgresql://postgres:pass123@localhost:5432/axiom"
    
    # JWT Authentication
    secret_key: str = "Kyv6FhtpTdB4gg01Owou2qYLgEwH63H-8ugbNS8Bf0g"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": False
    }


settings = Settings()

# Create database engine
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,  # Verify connections before using
    echo=False  # Set to True for SQL query logging
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for database models
Base = declarative_base()


def get_db():
    """
    Dependency function for FastAPI to get database session.
    
    Yields:
        Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

