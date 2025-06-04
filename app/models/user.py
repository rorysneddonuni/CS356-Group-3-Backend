from __future__ import annotations
import json
import pprint
from typing import Any, ClassVar, Dict, List, Optional, Literal
from datetime import datetime

from pydantic import BaseModel, Field, StrictInt, StrictStr

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self


class User(BaseModel):
    """
    User
    """
    id: Optional[StrictInt] = None
    username: Optional[StrictStr] = None
    first_name: Optional[StrictStr] = Field(default=None, alias="firstName")
    last_name: Optional[StrictStr] = Field(default=None, alias="lastName")
    email: Optional[StrictStr] = None
    password: Optional[StrictStr] = Field(
        default=None,
        exclude=True,
        description="Hashed password (never exposed in responses)"
    )
    role: Optional[Literal["unauthorised", "user", "admin", "superadmin"]] = "user"
    created_at: Optional[datetime] = Field(default=None, alias="createdAt")

    __properties: ClassVar[List[str]] = [
        "id",
        "username",
        "firstName",
        "lastName",
        "email",
        "role",
        "createdAt",
    ]

    model_config = {
        "populate_by_name": True,
        "validate_assignment": True,
    }

    def to_str(self) -> str:
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        return cls.model_validate(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        # Note: 'password' will be automatically excluded here
        return self.model_dump(by_alias=True, exclude_none=True)

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        if obj is None:
            return None
        return cls.model_validate(obj)
