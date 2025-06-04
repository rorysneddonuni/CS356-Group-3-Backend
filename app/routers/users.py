from typing import List

from fastapi import APIRouter, Body, HTTPException, Path, Depends
from pydantic import StrictStr
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated

from app.auth.dependencies import require_minimum_role, get_current_user, has_access_to_user
from app.database.database import get_db
from app.models.error import Error
from app.models.user import User
from app.models.user_input import UserInput
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
        UserInput,
        Body(
            ...,
            description="Data for new user; role is always set to 'user' and cannot be overridden",
        ),
    ],
    db: AsyncSession = Depends(get_db),
) -> User:
    if not UsersService.subclasses:
        raise HTTPException(status_code=501, detail="Not implemented")
    # enforce default role
    data = user_input.model_dump(exclude_none=True, by_alias=True)
    clean = UserInput.model_validate(data)
    return await UsersService.subclasses[0]().create_user(clean, db)


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
async def get_all_users(current_user: User = Depends(require_minimum_role("user")),
                        db: AsyncSession = Depends(get_db)) -> List[User]:
    if not UsersService.subclasses:
        raise HTTPException(status_code=501, detail="Not implemented")

    service = UsersService.subclasses[0]()

    if current_user.role == "user":
        # Just return their own data in a list
        user = await service.get_user_by_name(current_user.username, db)
        return [user] if user else []

    return await service.get_all_users(db)


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
    username: Annotated[StrictStr, Path(..., description="The username to fetch")],
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> User:
    if not has_access_to_user(current_user, username):
        raise HTTPException(status_code=401, detail="You can only access your own data")
    if not UsersService.subclasses:
        raise HTTPException(status_code=501, detail="Not implemented")
    return await UsersService.subclasses[0]().get_user_by_name(username, db)


@router.put(
    "/users/{username}",
    response_model=User,
    responses={
        200: {"model": User, "description": "Successful operation"},
        400: {"description": "Invalid input or conflict"},
        404: {"description": "User not found"},
        500: {"model": Error, "description": "Unexpected error"},
    },
    summary="Update user resource.",
    response_model_by_alias=True,
)
async def update_user(
    username: Annotated[StrictStr, Path(..., description="The username to update")],
    user_input: Annotated[
        UserInput,
        Body(..., description="Fields to update; only provided fields will change"),
    ],
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_minimum_role("admin")),
) -> User:
    if not UsersService.subclasses:
        raise HTTPException(status_code=501, detail="Not implemented")
    return await UsersService.subclasses[0]().update_user(username, user_input, db)


@router.delete(
    "/users/{username}",
    responses={
        204: {"description": "User deleted"},
        404: {"description": "User not found"},
        500: {"model": Error, "description": "Unexpected error"},
    },
    summary="Delete user resource.",
    response_model_by_alias=True,
)
async def delete_user(
    username: Annotated[StrictStr, Path(..., description="The username to delete")],
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_minimum_role("super_admin")),
) -> None:
    if not UsersService.subclasses:
        raise HTTPException(status_code=501, detail="Not implemented")
    await UsersService.subclasses[0]().delete_user(username, db)