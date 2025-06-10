from __future__ import annotations

import json
import pprint
from typing import Any, ClassVar, Dict, List, Optional, Tuple, Union

from pydantic import BaseModel, Field, StrictBytes, StrictInt, StrictStr

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self


class EncoderInput(BaseModel):
    """
    EncoderInput
    """  # noqa: E501
    id: Optional[StrictInt] = None
    name: Optional[StrictStr] = None
    comment: Optional[StrictStr] = None
    encoder_type: Optional[StrictStr] = Field(default=None, alias="encoderType")
    scalable: Optional[bool] = Field(default=False, alias="scalable")
    noOfLayers: Optional[StrictInt] = Field(default=None, alias="noOfLayers")
    path: Optional[StrictStr] = Field(default=False, alias="path")
    filename: Optional[StrictStr] = Field(default=None, alias="filename")
    modeFileReq: Optional[bool] = Field(default=False, alias="modeFileReq")
    seqFileReq: Optional[bool] = Field(default=False, alias="seqFileReq")
    layersFileReq: Optional[bool] = Field(default=False, alias="layersFileReq")
    __properties: ClassVar[List[str]] = ["id", "name", "encoderType", "scalable", "noOfLayers", "path", "filename", "modeFileReq", "seqFileReq", "layersFilesReq"]

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
        """Create an instance of EncoderInput from a JSON string"""
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
        """Create an instance of EncoderInput from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({"id": obj.get("id"), "name": obj.get("name"), "encoderType": obj.get("encoderType"),
                                   "encoderCode": obj.get("encoderCode"), "layers": obj.get("layers")})
        return _obj
