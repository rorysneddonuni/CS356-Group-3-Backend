from typing import Optional

from fastapi import APIRouter, Body, HTTPException, Path
from pydantic import Field, StrictStr
from typing_extensions import Annotated

from app.models.error import Error
from app.models.user import User
from app.models.user_input import UserInput
from app.services.users import UsersService

router = APIRouter()


@router.post("/users", responses={200: {"model": User, "description": "Successful operation"},
                                  200: {"model": Error, "description": "Unexpected error"}, }, tags=["users"],
             summary="Create a user.", response_model_by_alias=True, )
async def create_user(user_input: Annotated[
    Optional[UserInput], Field(description="User object creation and update in store")] = Body(None,
                                                                                               description="User object creation and update in store"), ) -> User:
    """This can only be done by the superuser."""
    if not UsersService.subclasses:
        raise HTTPException(status_code=501, detail="Not implemented")
    return await UsersService.subclasses[0]().create_user(user_input)


@router.delete("/users/{username}",
               responses={200: {"description": "User deleted"}, 400: {"description": "Invalid username supplied"},
                          404: {"description": "User not found"},
                          200: {"model": Error, "description": "Unexpected error"}, }, tags=["users"],
               summary="Delete user resource.", response_model_by_alias=True, )
async def delete_user(
        username: Annotated[StrictStr, Field(description="The username that needs to be deleted")] = Path(...,
                                                                                                          description="The username that needs to be deleted"), ) -> None:
    """This can only be done by the logged in user."""
    if not UsersService.subclasses:
        raise HTTPException(status_code=501, detail="Not implemented")
    return await UsersService.subclasses[0]().delete_user(username)


@router.get("/users/{username}", responses={200: {"model": User, "description": "Successful operation"},
                                            400: {"description": "Invalid username supplied"},
                                            404: {"description": "User not found"},
                                            200: {"model": Error, "description": "Unexpected error"}, }, tags=["users"],
            summary="Get user by username.", response_model_by_alias=True, )
async def get_user_by_name(username: Annotated[
    StrictStr, Field(description="The name that needs to be fetched. Use users1 for testing")] = Path(...,
                                                                                                      description="The name that needs to be fetched. Use users1 for testing"), ) -> User:
    """Get uses detail based on username."""
    if not UsersService.subclasses:
        raise HTTPException(status_code=501, detail="Not implemented")
    return await UsersService.subclasses[0]().get_user_by_name(username)


@router.put("/users/{username}",
            responses={200: {"description": "Successful operation"}, 400: {"description": "Bad request"},
                       404: {"description": "User not found"},
                       200: {"model": Error, "description": "Unexpected error"}, }, tags=["users"],
            summary="Update user resource.", response_model_by_alias=True, )
async def update_user(username: Annotated[StrictStr, Field(description="name that need to be deleted")] = Path(...,
                                                                                                               description="name that need to be deleted"),
                      user_input: Annotated[
                          Optional[UserInput], Field(description="User object creation and update in store")] = Body(
                          None, description="User object creation and update in store"), ) -> None:
    """This can only be done by the logged in user or superuser."""
    if not UsersService.subclasses:
        raise HTTPException(status_code=501, detail="Not implemented")
    return await UsersService.subclasses[0]().update_user(username, user_input)
