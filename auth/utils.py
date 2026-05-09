from fastapi import HTTPException, Depends
from starlette import status
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

# Local Import
from config import SECRET_KEY, ALGORITHM

AuthDependency = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_current_user(
    db,
    token: str = Depends(AuthDependency),
) -> str:
    try:
        local_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = local_token.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
            )
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
        )
