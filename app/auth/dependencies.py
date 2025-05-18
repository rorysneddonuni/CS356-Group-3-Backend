from typing import List, Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.models.user import User
from app.services.users import SqliteUsersService

SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login_form")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await SqliteUsersService().get_user_by_name(username, db)
    if user is None:
        raise credentials_exception

    if user.role != role:
        raise credentials_exception

    return user

def require_role(allowed_roles: list[str]):
    def checker(user: User = Depends(get_current_user)):
        if user.role not in allowed_roles:
            print(user.role)
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return checker