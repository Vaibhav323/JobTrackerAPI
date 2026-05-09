from pydantic import BaseModel, EmailStr, field_validator
import datetime as dt
import string


class AuthUserRequest(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 character long")
        if not any(ch.islower() for ch in v):
            raise ValueError("Password must contain a lowercase letter")
        if not any(ch.isupper() for ch in v):
            raise ValueError("Password must contain a uppercase letter")
        if not any(ch.isdigit() for ch in v):
            raise ValueError("Password must contain a digit")
        if not any(ch in string.punctuation for ch in v):
            raise ValueError("Password must contain a special character")
        return v


class RefreshTokenRequest(BaseModel):
    refresh_token: str


# Response Models
class RegisterResponse(BaseModel):
    id: str
    user_email: EmailStr
    created_at: dt.datetime


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
