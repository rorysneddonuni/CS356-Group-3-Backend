import logging
from typing import ClassVar, Tuple, List, Optional

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
            c.key: getattr(obj, c.key).value
            if isinstance(getattr(obj, c.key), enum.Enum)
            else getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs
        }

    async def create_user(self, user_input: UserInput, db: AsyncSession) -> User:
        logger.info(f"Creating user: {user_input.username}")
        # ensure username/email unique
        result = await db.execute(
            select(user_table).where(
                or_(
                    user_table.username == user_input.username,
                    user_table.email == user_input.email,
                )
            )
        )
        existing = result.scalars().first()
        if existing:
            if existing.username == user_input.username:
                raise HTTPException(status_code=400, detail="Username already exists")
            raise HTTPException(status_code=400, detail="Email already registered")

        data = user_input.model_dump(exclude_none=True, by_alias=True)
        data["password"] = pwd_context.hash(data["password"])
        db_obj = user_table(**data)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return User.model_validate(self.safe_dict(db_obj))

    async def get_all_users(self, db: AsyncSession, roles: Optional[List[str]] = None) -> List[User]:
        logger.info("Retrieving all users")
        query = select(user_table)

        if roles:
            query = query.where(user_table.role.in_(roles))

        result = await db.execute(query)
        users: List[User] = []
        for obj in result.scalars().all():
            users.append(User.model_validate(self.safe_dict(obj)))
        return users

    async def get_user_by_name(self, username: str, db: AsyncSession) -> User:
        logger.info(f"Retrieving user: {username}")
        result = await db.execute(
            select(user_table).where(user_table.username == username)
        )
        db_obj = result.scalars().first()
        if not db_obj:
            raise HTTPException(status_code=404, detail="User not found")
        return User.model_validate(self.safe_dict(db_obj))

    async def get_user_by_email(self, email: str, db: AsyncSession) -> User:
        logger.info(f"Retrieving user by email: {email}")
        result = await db.execute(
            select(user_table).where(user_table.email == email)
        )
        db_obj = result.scalars().first()
        if not db_obj:
            raise HTTPException(status_code=404, detail="User not found")
        return User.model_validate(self.safe_dict(db_obj))

    async def update_user(self, username: str, user_input: UserInput, db: AsyncSession) -> User:
        logger.info(f"Updating user: {username}")
        result = await db.execute(
            select(user_table).where(user_table.username == username)
        )
        db_obj = result.scalars().first()
        if not db_obj:
            raise HTTPException(status_code=404, detail="User not found")

        update_data = user_input.model_dump(exclude_none=True, by_alias=True)

        # username conflict?
        if "username" in update_data and update_data["username"] != username:
            dup = await db.execute(
                select(user_table).where(
                    user_table.username == update_data["username"]
                )
            )
            if dup.scalars().first():
                raise HTTPException(status_code=400, detail="Username already exists")
        # email conflict?
        if "email" in update_data and update_data["email"] != db_obj.email:
            dup = await db.execute(
                select(user_table).where(
                    user_table.email == update_data["email"]
                )
            )
            if dup.scalars().first():
                raise HTTPException(status_code=400, detail="Email already registered")

        if "password" in update_data:
            update_data["password"] = pwd_context.hash(update_data["password"])

        for key, val in update_data.items():
            setattr(db_obj, key, val)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return User.model_validate(self.safe_dict(db_obj))

    async def delete_user(self, username: str, db: AsyncSession) -> Response:
        logger.info(f"Deleting user: {username}")
        result = await db.execute(
            select(user_table).where(user_table.username == username)
        )
        db_obj = result.scalars().first()
        if not db_obj:
            raise HTTPException(status_code=404, detail="User not found")

        await db.delete(db_obj)
        await db.commit()
        return Response(status_code=204)


    async def update_password(self, email: str, hashed_password: str, db: AsyncSession) -> None:
        logger.info(f"Updating password for: {email}")
        result = await db.execute(
            select(user_table).where(user_table.email == email)
        )
        db_obj = result.scalars().first()
        if not db_obj:
            raise HTTPException(status_code=404, detail="User not found")

        db_obj.password = hashed_password

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

    async def get_user_role_by_id(self, user_id: int, db: AsyncSession) -> str:
        result = await db.execute(
            select(user_table).where(user_table.id == user_id)
        )
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user.role.value


class SqliteUsersService(UsersService):
    pass