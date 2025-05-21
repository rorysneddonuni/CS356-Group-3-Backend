# app/routers/users.py

from typing import List

from fastapi import APIRouter, Body, HTTPException, Path, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import StrictStr, Field
from typing_extensions import Annotated

from app.database.database import get_db
from app.models.error import Error
from app.models.user import User
from app.models.user_input import CreateUserInput, UpdateUserInput
from app.services.users import UsersService

router = APIRouter(tags=["users"])


@router.post(
    "/users",
    response_model=User,
    responses={
        200: {"model": User, "description": "Successful operation"},
        500: {"model": Error, "description": "Unexpected error"},
    },
    summary="Create a user.",
    response_model_by_alias=True,
)
async def create_user(
    user_input: Annotated[
        CreateUserInput, Body(..., description="Data for new user (role fixed to 'user')")
    ],
    db: AsyncSession = Depends(get_db),
) -> User:
    if not UsersService.subclasses:
        raise HTTPException(status_code=501, detail="Not implemented")
    return await UsersService.subclasses[0]().create_user(user_input, db)


@router.get(
    "/users",
    response_model=List[User],
    responses={
        200: {"model": List[User], "description": "Successful operation"},
        500: {"model": Error, "description": "Unexpected error"},
    },
    summary="Get all users.",
    response_model_by_alias=True,
)
async def get_all_users(db: AsyncSession = Depends(get_db)) -> List[User]:
    if not UsersService.subclasses:
        raise HTTPException(status_code=501, detail="Not implemented")
    return await UsersService.subclasses[0]().get_all_users(db)


@router.get(
    "/users/{username}",
    response_model=User,
    responses={
        200: {"model": User, "description": "Successful operation"},
        404: {"description": "User not found"},
        500: {"model": Error, "description": "Unexpected error"},
    },
    summary="Get user by username.",
    response_model_by_alias=True,
)
async def get_user_by_username(
    username: Annotated[str, Path(..., description="The username to fetch")],
    db: AsyncSession = Depends(get_db),
) -> User:
    if not UsersService.subclasses:
        raise HTTPException(status_code=501, detail="Not implemented")
    return await UsersService.subclasses[0]().get_user_by_name(username, db)


@router.get(
    "/users/id/{user_id}",
    response_model=User,
    responses={
        200: {"model": User, "description": "Successful operation"},
        404: {"description": "User not found"},
        500: {"model": Error, "description": "Unexpected error"},
    },
    summary="Get user by ID.",
    response_model_by_alias=True,
)
async def get_user_by_id(
    user_id: Annotated[int, Path(..., description="The user ID to fetch")],
    db: AsyncSession = Depends(get_db),
) -> User:
    if not UsersService.subclasses:
        raise HTTPException(status_code=501, detail="Not implemented")
    return await UsersService.subclasses[0]().get_user_by_id(user_id, db)


@router.get(
    "/users/email/{email}",
    response_model=User,
    responses={
        200: {"model": User, "description": "Successful operation"},
        404: {"description": "User not found"},
        500: {"model": Error, "description": "Unexpected error"},
    },
    summary="Get user by email.",
    response_model_by_alias=True,
)
async def get_user_by_email(
    email: Annotated[str, Path(..., description="The email to fetch")],
    db: AsyncSession = Depends(get_db),
) -> User:
    if not UsersService.subclasses:
        raise HTTPException(status_code=501, detail="Not implemented")
    return await UsersService.subclasses[0]().get_user_by_email(email, db)


@router.put(
    "/users/{user_id}",
    response_model=User,
    responses={
        200: {"model": User, "description": "Successful operation"},
        404: {"description": "User not found"},
        500: {"model": Error, "description": "Unexpected error"},
    },
    summary="Update user resource.",
    response_model_by_alias=True,
)
async def update_user(
    user_id: Annotated[int, Path(..., description="The user ID to update")],
    user_input: Annotated[
        UpdateUserInput, Body(..., description="Fields to update; role allowed if needed")
    ],
    db: AsyncSession = Depends(get_db),
) -> User:
    if not UsersService.subclasses:
        raise HTTPException(status_code=501, detail="Not implemented")
    return await UsersService.subclasses[0]().update_user(user_id, user_input, db)


@router.delete(
    "/users/{user_id}",
    responses={
        204: {"description": "User deleted"},
        404: {"description": "User not found"},
        500: {"model": Error, "description": "Unexpected error"},
    },
    summary="Delete user resource.",
    response_model_by_alias=True,
)
async def delete_user(
    user_id: Annotated[int, Path(..., description="The user ID to delete")],
    db: AsyncSession = Depends(get_db),
) -> None:
    if not UsersService.subclasses:
        raise HTTPException(status_code=501, detail="Not implemented")
    await UsersService.subclasses[0]().delete_user(user_id, db)