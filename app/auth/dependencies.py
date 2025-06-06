from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.config import SECRET_KEY, ALGORITHM, ROLE_HIERARCHY
from app.database.database import get_db
from app.models.user import User
from app.services.users import SqliteUsersService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token, please regenerate using auth endpoint",
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

def has_access_to_user(requesting_user: User, target_username: str) -> bool:
    if requesting_user.role in ("admin", "super_admin"):
        return True
    return requesting_user.username == target_username

def require_minimum_role(min_role: str):
    def checker(user: User = Depends(get_current_user)) -> User:
        user_level = ROLE_HIERARCHY.get(user.role, 0)
        required_level = ROLE_HIERARCHY.get(min_role, 0)

        if user_level < required_level:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. '{min_role}' or higher required."
            )
        return user
    return checker
