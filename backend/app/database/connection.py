import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    connect_args={},  # For PostgreSQL you usually don't need extra args
)

# Create a configured "Session" class
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for models
Base = declarative_base()

# Dependency function for FastAPI routes
def get_db():
    """
    Yields a SQLAlchemy session, and ensures it is closed after use.
    Use this as a dependency in FastAPI routes:
    
        from fastapi import Depends
        from app.database.connection import get_db

        def my_route(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
