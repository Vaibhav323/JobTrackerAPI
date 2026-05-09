from database import Base
from sqlalchemy import Column, String, Boolean, DateTime, func, ForeignKey
from uuid import uuid4


class RefreshToken(Base):
    __tablename__ = "refresh_token"

    id = Column(
        String,
        nullable=False,
        unique=True,
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    user_id = Column(String, ForeignKey("users.id"))
    token_hash = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    revoked_at = Column(DateTime)
