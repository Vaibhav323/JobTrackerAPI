from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from jose import jwt

import datetime as dt

# Local Import
from config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from database import db_dependency
from models import User, RefreshToken
from auth.utils import bcrypt_context, get_current_user, AuthDependency
from auth.service import create_refresh_token
from auth.schemas import (
    RegisterResponse,
    RefreshTokenRequest,
    LoginResponse,
    AuthUserRequest,
)

router = APIRouter()


@router.post(
    "/api/v1/auth/register",
    tags=["Authentication"],
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(create_user_request: AuthUserRequest, db: db_dependency):
    """Register a new user account.

    Checks for duplicate email before inserting. Password is hashed
    with bcrypt before being stored.

    Args:
        create_user_request: Request body containing email and password.
        db: Active database session injected by FastAPI dependency.

    Returns:
        RegisterResponse: The new user's id, email, and created_at timestamp.

    Raises:
        HTTPException: 409 if the email is already registered.
    """
    search_user = (
        db.query(User).filter(User.user_email == create_user_request.email).first()
    )
    if search_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists!"
        )
    new_user = User(
        user_email=create_user_request.email,
        password_hash=bcrypt_context.hash(create_user_request.password),
        created_at=dt.datetime.now(dt.timezone.utc),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post(
    "/api/v1/auth/login",
    tags=["Authentication"],
    status_code=status.HTTP_202_ACCEPTED,
    response_model=LoginResponse,
)
async def login_user(db: db_dependency, login_user_request: AuthUserRequest):
    """Login the user account.

    Checks for email exists and password is matching or not from db. After
    successful verification, generates access token, refresh token and token
    type.

    Args:
        login_user_request: Request body containing email and password.
        db: Active database session injected by FastAPI dependency.

    Returns:
        LoginResponse: access token, refresh token and token type.

    Raises:
        HTTPException: 401 if the credentials are invalid.
    """
    exist_user = (
        db.query(User).filter(User.user_email == login_user_request.email).first()
    )
    if not exist_user or not bcrypt_context.verify(
        login_user_request.password, exist_user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )
    access_token_time = dt.datetime.now(dt.timezone.utc) + dt.timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = jwt.encode(
        {"sub": exist_user.id, "exp": access_token_time},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    refresh_token = create_refresh_token(exist_user.id, db)
    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )


@router.post(
    "/api/v1/auth/refresh",
    tags=["Authentication"],
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
)
async def token_refresh(request: RefreshTokenRequest, db: db_dependency):
    """Exchange a refresh token for a new access and refresh token pair.

    Validates the token exists in database, is not expired and revoked value is None.
    After successfully validating the token, mark the token as revoked and assign
    new access token and refresh token

    Args:
        request: Request body containing the refresh token string.
        db: Active database session injected by FastAPI dependency.

    Returns:
        LoginResponse: access token, refresh token and token type.

    Raises:
        HTTPException: 401 if the token is invalid.
    """
    search_token = db.query(RefreshToken).filter(RefreshToken.revoked_at == None).all()
    db_token = None
    for token in search_token:
        if bcrypt_context.verify(request.refresh_token, token.token_hash):
            db_token = token
            break

    if not db_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token",
        )

    if (
        db_token.expires_at <= dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
        or db_token.revoked_at is not None
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token",
        )
    db_token.revoked_at = dt.datetime.now(dt.timezone.utc)
    access_token_time = dt.datetime.now(dt.timezone.utc) + dt.timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = jwt.encode(
        {"sub": db_token.user_id, "exp": access_token_time},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    refresh_token = create_refresh_token(db_token.user_id, db)
    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )


@router.post(
    "/api/v1/auth/logout",
    tags=["Authentication"],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def logout_user(db: db_dependency, token=Depends(AuthDependency)):
    """Logout user from all session

    Fetch user id using `get_current_user` function and revoked each token
    from the database

    Args:
        token: Request body containing access token
        db: Active database session injected by FastAPI dependency.

    Raises:
        HTTPException: 401 if the access token is missing or invalid.
    """
    fetch_user_id = get_current_user(db, token)
    user_session = (
        db.query(RefreshToken).filter(RefreshToken.user_id == fetch_user_id).all()
    )
    for session in user_session:
        session.revoked_at = dt.datetime.now(dt.timezone.utc)
    db.commit()
