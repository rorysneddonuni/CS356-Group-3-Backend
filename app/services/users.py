import logging
from typing import ClassVar, Tuple, List

from fastapi import HTTPException
from fastapi.responses import Response
from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.inspection import inspect
from passlib.context import CryptContext
import enum

from app.database.tables.user import User as user_table
from app.models.user import User
from app.models.user_input import UserInput

logger = logging.getLogger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UsersService:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        UsersService.subclasses += (cls,)

    def safe_dict(self, obj):
        return {
            c.key: getattr(obj, c.key).value if isinstance(getattr(obj, c.key), enum.Enum) else getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs
        }

    async def create_user(self, user_input: UserInput, db: AsyncSession) -> User:
        logger.info(f"Creating user: {user_input.username}")
        result = await db.execute(select(user_table).where(
            or_(user_table.username == user_input.username, user_table.email == user_input.email)))
        existing = result.scalars().first()
        if existing:
            if existing.username == user_input.username:
                raise HTTPException(status_code=400, detail="Username already exists")
            raise HTTPException(status_code=400, detail="Email already registered")

        user_data = user_input.model_dump(exclude_none=True)
        user_data["password"] = pwd_context.hash(user_data["password"])
        db_obj = user_table(**user_data)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return User.model_validate(self.safe_dict(db_obj))

    async def get_user_by_name(self, username: str, db: AsyncSession) -> User:
        logger.info(f"Retrieving user: {username}")
        result = await db.execute(select(user_table).where(user_table.username == username))
        db_obj = result.scalars().first()
        if not db_obj:
            raise HTTPException(status_code=404, detail="User not found")
        return User.model_validate(self.safe_dict(db_obj))

    async def get_user_by_email(self, email: str, db: AsyncSession) -> User:
        logger.info(f"Retrieving user by email: {email}")
        result = await db.execute(select(user_table).where(user_table.email == email))
        db_obj = result.scalars().first()
        if not db_obj:
            raise HTTPException(status_code=404, detail="User not found")
        return User.model_validate(self.safe_dict(db_obj))

    async def get_user_by_id(self, user_id: int, db: AsyncSession) -> User:
        logger.info(f"Retrieving user by id: {user_id}")
        result = await db.execute(select(user_table).where(user_table.id == user_id))
        db_obj = result.scalars().first()
        if not db_obj:
            raise HTTPException(status_code=404, detail="User not found")
        return User.model_validate(self.safe_dict(db_obj))

    async def get_all_users(self, db: AsyncSession) -> List[User]:
        logger.info("Retrieving all users")
        result = await db.execute(select(user_table))
        db_objs = result.scalars().all()
        users: List[User] = []
        for obj in db_objs:
            data = self.safe_dict(obj)
            data.pop("password", None)
            users.append(User.model_validate(data))
        return users

    async def update_user(self, username: str, user_input: UserInput, db: AsyncSession) -> User:
        logger.info(f"Updating user: {username}")
        result = await db.execute(select(user_table).where(user_table.username == username))
        db_obj = result.scalars().first()
        if not db_obj:
            raise HTTPException(status_code=404, detail="User not found")

        update_data = user_input.model_dump(exclude_none=True)
        # Prevent changing immutable fields
        for field in ("id", "username", "email"):
            update_data.pop(field, None)

        # Hash password if it's being updated
        if "password" in update_data:
            update_data["password"] = pwd_context.hash(update_data["password"])

        for key, value in update_data.items():
            setattr(db_obj, key, value)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return User.model_validate(self.safe_dict(db_obj))

    async def delete_user(self, username: str, db: AsyncSession) -> Response:
        logger.info(f"Deleting user: {username}")
        result = await db.execute(select(user_table).where(user_table.username == username))
        db_obj = result.scalars().first()
        if not db_obj:
            raise HTTPException(status_code=404, detail="User not found")

        await db.delete(db_obj)
        await db.commit()
        return Response(status_code=204)


class SqliteUsersService(UsersService):
    pass
