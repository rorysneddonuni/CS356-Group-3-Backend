from __future__ import annotations

import json
import pprint
from typing import Any, ClassVar, Dict, List, Optional, Tuple, Union

from pydantic import BaseModel, Field, StrictBytes, StrictInt, StrictStr

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self


class Encoder(BaseModel):
    """
    Encoder
    """
    id: Optional[StrictInt] = None
    name: Optional[StrictStr] = None
    encoder_type: Optional[StrictStr] = Field(default=None, alias="encoderType")
    encoder_code: Optional[StrictStr] = Field(default=None, alias="encoderCode")
    layers: Optional[List[Union[StrictBytes, StrictStr, Tuple[StrictStr, StrictBytes]]]] = None

    __properties: ClassVar[List[str]] = ["id", "name", "encoderType", "encoderCode", "layers"]

    model_config = {
        "populate_by_name": True,
        "validate_assignment": True,
        "protected_namespaces": (),
    }

    def to_str(self) -> str:
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(by_alias=True, exclude_none=True)

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        if obj is None:
            return None
        if not isinstance(obj, dict):
            return cls.model_validate(obj)
        return cls.model_validate({
            "id": obj.get("id"),
            "name": obj.get("name"),
            "encoderType": obj.get("encoderType"),
            "encoderCode": obj.get("encoderCode"),
            "layers": obj.get("layers"),
        })