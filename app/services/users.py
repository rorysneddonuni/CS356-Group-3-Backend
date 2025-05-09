from typing import ClassVar, Tuple, Optional
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.user       import User        as PydanticUser
from app.models.user_input import UserInput
from app.database.tables.user  import UserTable


class UsersService:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        UsersService.subclasses += (cls,)

    async def create_user(
        self,
        user_input: UserInput,
        db: AsyncSession
    ) -> PydanticUser:
        # Dump only the fields the user actually set
        data = user_input.model_dump(exclude_none=True)
        db_obj = UserTable(**data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        # Convert the ORM object dict into your Pydantic model
        return PydanticUser.model_validate(db_obj.__dict__)

    async def get_user_by_name(
        self,
        username: str,
        db: AsyncSession
    ) -> PydanticUser:
        result = await db.execute(
            select(UserTable).where(UserTable.username == username)
        )
        db_obj = result.scalars().first()
        if not db_obj:
            raise HTTPException(status_code=404, detail="User not found")
        return PydanticUser.model_validate(db_obj.__dict__)

    async def update_user(
        self,
        username: str,
        user_input: UserInput,
        db: AsyncSession
    ) -> None:
        result = await db.execute(
            select(UserTable).where(UserTable.username == username)
        )
        db_obj = result.scalars().first()
        if not db_obj:
            raise HTTPException(status_code=404, detail="User not found")

        updates = user_input.model_dump(exclude_none=True)
        for field, value in updates.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        await db.commit()

    async def delete_user(
        self,
        username: str,
        db: AsyncSession
    ) -> None:
        result = await db.execute(
            select(UserTable).where(UserTable.username == username)
        )
        db_obj = result.scalars().first()
        if not db_obj:
            raise HTTPException(status_code=404, detail="User not found")

        await db.delete(db_obj)
        await db.commit()


# Register the concrete implementation so that
# UsersService.subclasses[0] is this one:
class SqliteUsersService(UsersService):
    pass