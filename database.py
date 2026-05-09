from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from typing import Annotated

# Local Import
from config import DATABASE_URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


def get_db():
    """
    FastAPI dependency that provides a SQLAlchemy database session.

    - Opens a new session at the start of each request
    - Yields the session for use in route handlers
    - Guarantees the session is closed after the request completes,
      even if an exception is raised
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
Base.metadata.create_all(bind=engine)
