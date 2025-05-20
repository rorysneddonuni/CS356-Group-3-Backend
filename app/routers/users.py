from typing import List, Optional

from fastapi import APIRouter, Body, HTTPException, Path, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import Field, StrictStr
from typing_extensions import Annotated

from app.auth.dependencies import require_role
from app.database.database import get_db
from app.models.error import Error
from app.models.user import User
from app.models.user_input import UserInput
from app.services.users import UsersService

router = APIRouter(tags=["users"])

# Create a new user (public)
# Create a new user (public) — ignore any supplied role
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
        Optional[UserInput], Field(..., description="User object creation in store")
    ] = Body(...),
    db: AsyncSession = Depends(get_db),
) -> User:
    if not UsersService.subclasses:
        raise HTTPException(status_code=501, detail="Not implemented")
    # Strip out any client-supplied role so default 'user' is used
    data = user_input.model_dump(exclude_none=True)
    data.pop("role", None)
    clean_input = UserInput.model_validate(data)
    return await UsersService.subclasses[0]().create_user(clean_input, db)

# List all users (public)
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
async def get_all_users(
    db: AsyncSession = Depends(get_db),
) -> List[User]:
    if not UsersService.subclasses:
        raise HTTPException(status_code=501, detail="Not implemented")
    return await UsersService.subclasses[0]().get_all_users(db)

# Retrieve a user by username (public)
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
    username: Annotated[str, Path(..., description="The username that needs to be fetched")],
    db: AsyncSession = Depends(get_db),
) -> User:
    if not UsersService.subclasses:
        raise HTTPException(status_code=501, detail="Not implemented")
    return await UsersService.subclasses[0]().get_user_by_name(username, db)

# Retrieve a user by user ID (public)
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
    user_id: Annotated[int, Path(..., description="The ID of the user to fetch")],
    db: AsyncSession = Depends(get_db),
) -> User:
    if not UsersService.subclasses:
        raise HTTPException(status_code=501, detail="Not implemented")
    return await UsersService.subclasses[0]().get_user_by_id(user_id, db)

# Retrieve a user by email (public)
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
    email: Annotated[str, Path(..., description="The email address of the user to fetch")],
    db: AsyncSession = Depends(get_db),
) -> User:
    if not UsersService.subclasses:
        raise HTTPException(status_code=501, detail="Not implemented")
    return await UsersService.subclasses[0]().get_user_by_email(email, db)

# Update a user (self only)
@router.put(
    "/users/{username}",
    response_model=User,
    responses={
        200: {"model": User, "description": "Successful operation"},
        403: {"description": "Forbidden"},
        404: {"description": "User not found"},
        500: {"model": Error, "description": "Unexpected error"},
    },
    summary="Update user resource.",
    response_model_by_alias=True,
)
async def update_user(
    username: Annotated[StrictStr, Path(..., description="The username to update")],
    user_input: Annotated[
        Optional[UserInput], Body(..., description="User object creation and update in store")
    ],
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(["user", "admin", "superadmin"]))
) -> User:
    # Allow normal users to update only their own record
    if current_user.role == "user" and current_user.username != username:
        raise HTTPException(status_code=403, detail="Users can only update their own profile")
    if not UsersService.subclasses:
        raise HTTPException(status_code=501, detail="Not implemented")
    return await UsersService.subclasses[0]().update_user(username, user_input, db)

# Delete a user (admin & superadmin only)
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
    current_user: User = Depends(require_role(["admin", "superadmin"]))
) -> None:
    if not UsersService.subclasses:
        raise HTTPException(status_code=501, detail="Not implemented")
    await UsersService.subclasses[0]().delete_user(username, db)
