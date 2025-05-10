from typing import ClassVar, Tuple

from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database.tables.user import UserTable
from app.models.user import User
from app.models.user_input import UserInput


class UsersService:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        UsersService.subclasses += (cls,)

    async def create_user(self, user_input: UserInput, db: AsyncSession) -> User:
        # Check if username or email already exists
        result = await db.execute(select(UserTable).where(
            or_(UserTable.username == user_input.username, UserTable.email == user_input.email)))
        existing = result.scalars().first()
        if existing:
            if existing.username == user_input.username:
                raise HTTPException(status_code=400, detail="Username already exists")
            else:
                raise HTTPException(status_code=400, detail="Email already registered")

        # Create and save user
        db_obj = UserTable(**user_input.model_dump(exclude_none=True))
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        return User.model_validate(db_obj.__dict__)

    async def get_user_by_name(self, username: str, db: AsyncSession) -> User:
        result = await db.execute(select(UserTable).where(UserTable.username == username))
        db_obj = result.scalars().first()
        if not db_obj:
            raise HTTPException(status_code=404, detail="User not found")
        return User.model_validate(db_obj.__dict__)

    async def update_user(self, username: str, user_input: UserInput, db: AsyncSession) -> None:
        result = await db.execute(select(UserTable).where(UserTable.username == username))
        db_obj = result.scalars().first()
        if not db_obj:
            raise HTTPException(status_code=404, detail="User not found")

        updates = user_input.model_dump(exclude_none=True)
        for field, value in updates.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        await db.commit()
        return User.model_validate(db_obj.__dict__)

    async def delete_user(self, username: str, db: AsyncSession) -> None:
        result = await db.execute(select(UserTable).where(UserTable.username == username))
        db_obj = result.scalars().first()
        if not db_obj:
            raise HTTPException(status_code=404, detail="User not found")

        await db.delete(db_obj)
        await db.commit()
        return JSONResponse(status_code=200, content={"message": "User deleted"})


# Register the concrete implementation so that
# UsersService.subclasses[0] is this one:
class SqliteUsersService(UsersService):
    pass
