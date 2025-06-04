from datetime import datetime, timedelta
from typing import ClassVar, Tuple, Optional

from jose import jwt
from fastapi import HTTPException, status
from passlib.context import CryptContext

from app.auth.config import ALGORITHM, SECRET_KEY
from app.models.login_request import LoginRequest
from app.models.login_response import LoginResponse
from app.models.user import User
from app.services.users import SqliteUsersService

ACCESS_TOKEN_EXPIRE_MINUTES = 60
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class BaseAuthApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseAuthApi.subclasses += (cls,)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": int(expire.timestamp())})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    async def login_user(self, login_request: LoginRequest, db) -> LoginResponse:
        raise NotImplementedError("login_user must be implemented in a subclass")


class AuthService(BaseAuthApi):
    async def login_user(self, login_request: LoginRequest, db) -> LoginResponse:
        """Authenticate a user with username and password."""
        user: Optional[User] = await SqliteUsersService().get_user_by_name(login_request.username, db)
        if not user or not self.verify_password(login_request.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
        issued_at = int(datetime.utcnow().timestamp())
        payload = {
            "sub": user.username,
            "role": user.role,
            "issued_at": issued_at,
            "firstname": user.first_name,
            "surname": user.last_name,
            "username": user.username,
        }
        token = self.create_access_token(payload)
        return LoginResponse(token=token)
