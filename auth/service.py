from fastapi import HTTPException
from starlette import status
import datetime as dt
import secrets

# UTIL Function
from auth.utils import bcrypt_context
from models import User, RefreshToken


def create_refresh_token(user_id: str, db) -> str:
    # Security Concerns
    check_user = db.query(User).filter(User.id == user_id).first()
    if not check_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User does not exist!"
        )
    refresh_token = secrets.token_urlsafe(64)
    db_token = RefreshToken(
        user_id=user_id,
        token_hash=bcrypt_context.hash(refresh_token),
        created_at=dt.datetime.now(dt.timezone.utc),
        expires_at=dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=7),
    )
    db.add(db_token)
    db.commit()
    return refresh_token
