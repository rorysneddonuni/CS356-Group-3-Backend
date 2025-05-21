from __future__ import annotations

import json
import pprint
from typing import Any, ClassVar, Dict, List, Optional, Literal

from pydantic import BaseModel, Field, StrictStr

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self


class CreateUserInput(BaseModel):
    """
    Schema for creating a user.
    Excludes `role` to prevent clients from setting it manually.
    """
    username: StrictStr = Field(..., description="Unique username, 50 characters max")
    first_name: StrictStr = Field(..., alias="first_name", description="User's first name")
    last_name: StrictStr = Field(..., alias="last_name", description="User's last name")
    email: StrictStr = Field(..., description="Unique email address")
    password: StrictStr = Field(..., description="User password, will be hashed before storage")

    __properties: ClassVar[List[str]] = ["username", "first_name", "last_name", "email", "password"]
    model_config = {"populate_by_name": True, "validate_assignment": True}

    def to_str(self) -> str:
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        return json.dumps(self.model_dump(by_alias=True, exclude_none=True))

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        return cls.model_validate_json(json_str)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(by_alias=True, exclude_none=True)

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        if obj is None:
            return None
        return cls.model_validate(obj)


class UpdateUserInput(BaseModel):
    """
    Schema for updating a user.
    Allows clients (with sufficient privileges) to update role.
    """
    username: Optional[StrictStr] = None
    first_name: Optional[StrictStr] = Field(default=None, alias="first_name")
    last_name: Optional[StrictStr] = Field(default=None, alias="last_name")
    email: Optional[StrictStr] = None
    password: Optional[StrictStr] = None
    role: Optional[Literal["user", "admin", "superadmin"]] = None

    __properties: ClassVar[List[str]] = [
        "username", "first_name", "last_name", "email", "password", "role"
    ]
    model_config = {"populate_by_name": True, "validate_assignment": True}

    def to_str(self) -> str:
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        return json.dumps(self.model_dump(by_alias=True, exclude_none=True))

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        return cls.model_validate_json(json_str)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(by_alias=True, exclude_none=True)

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        if obj is None:
            return None
        return cls.model_validate(obj)