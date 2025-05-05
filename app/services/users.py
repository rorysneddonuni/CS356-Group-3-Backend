from typing import ClassVar, Tuple
from typing import Optional

from pydantic import Field, StrictStr
from typing_extensions import Annotated

from app.models.user import User
from app.models.user_input import UserInput


class UsersService:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        UsersService.subclasses = UsersService.subclasses + (cls,)

    async def create_user(self, user_input: Annotated[
        Optional[UserInput], Field(description="User object creation and update in store")], ) -> User:
        """This can only be done by the superuser."""
        ...

    async def delete_user(self, username: Annotated[
        StrictStr, Field(description="The username that needs to be deleted")], ) -> None:
        """This can only be done by the logged in user."""
        ...

    async def get_user_by_name(self, username: Annotated[
        StrictStr, Field(description="The name that needs to be fetched. Use users1 for testing")], ) -> User:
        """Get uses detail based on username."""
        ...

    async def update_user(self, username: Annotated[StrictStr, Field(description="name that need to be deleted")],
                          user_input: Annotated[Optional[UserInput], Field(
                              description="User object creation and update in store")], ) -> None:
        """This can only be done by the logged in user or superuser."""
        ...
