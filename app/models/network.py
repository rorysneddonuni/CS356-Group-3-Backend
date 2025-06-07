from __future__ import annotations

import json
import pprint
from typing import Any, ClassVar, Dict, List, Optional

from pydantic import BaseModel, Field, StrictInt, StrictStr

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self


class Network(BaseModel):
    """
    Network
    """  # noqa: E501
    id: Optional[StrictInt] = None
    name: Optional[StrictStr] = Field(None, alias="name")
    packet_loss: Optional[StrictInt] = Field(default=None, alias="packetLoss")
    delay: Optional[StrictInt] = Field(default=None, alias="delay")
    jitter: Optional[StrictInt] = Field(default=None, alias="jitter")
    bandwidth: Optional[StrictInt] = Field(default=None, alias="bandwidth")
    __properties: ClassVar[List[str]] = ["id", "name", "packet_loss", "delay", "jitter", "bandwidth"]

    model_config = {"populate_by_name": True, "validate_assignment": True, "protected_namespaces": (), }

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of Network from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        _dict = self.model_dump(by_alias=True, exclude={}, exclude_none=True, )
        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of Network from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({"id": obj.get("id"), "name": obj.get("name"), "networkType": obj.get("networkType")})
        return _obj
