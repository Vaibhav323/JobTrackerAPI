from database import Base
from sqlalchemy import Column, String, Boolean, DateTime, func
from uuid import uuid4


class User(Base):
    __tablename__ = "users"

    id = Column(
        String,
        nullable=False,
        unique=True,
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    user_email = Column(String, nullable=False, index=True, unique=True)
    password_hash = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
