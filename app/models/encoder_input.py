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
    video_id: Optional[StrictStr] = None
    duration: Optional[StrictInt] = None
    frames_to_encode: Optional[StrictInt] = None
    fps: Optional[StrictInt] = None
    res_width: Optional[StrictInt] = None
    res_height: Optional[StrictInt] = None
    input_file_title: Optional[StrictStr] = None
    encoder: Optional[StrictStr] = None
    encoder_type: Optional[StrictStr] = Field(default=None, alias="encoderType")
    bit_rate: Optional[StrictInt] = None
    yuv_format: Optional[StrictStr] = None
    encoder_mode: Optional[StrictStr] = None
    quality: Optional[StrictInt] = None
    bit_depth: Optional[StrictInt] = None
    infrared_period: Optional[StrictInt] = None
    b_frames: Optional[StrictInt] = None
    max_no_layers: Optional[StrictInt] = None

    __properties: ClassVar[List[str]] = ["id", "video_id", "duration", "frames_to_encode", "fps", "res_width",
                                         "res_height",
                                         "input_file_title", "encoder", "encoder_type", "bit_rate", "yuv_format",
                                         "encoder_mode",
                                         "quality", "bit_depth", "infrared_period", "b_frames", "max_no_layers"]
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

        _obj = cls.model_validate({"id": obj.get("id"), "video_id": obj.get("video_id"), "duration": obj.get("duration"), "frames_to_encode": obj.get("frames_to_encode"), "fps": obj.get("fps"), "res_width": obj.get("res_width"),
                                   "res_height": obj.get("res_height"), "input_file_title": obj.get("input_file_title"), "encoder": obj.get("encoder"), "encoder_type": obj.get("encoder_type"), "bit_rate": obj.get("bit_rate"),
                                   "yuv_format": obj.get("yuv_format"), "encoder_mode": obj.get("encoder_mode"), "quality": obj.get("quality"), "bit_depth": obj.get("bit_depth"), "infrared_period": obj.get("infrared_period"),
                                   "b_frames": obj.get("b_frames"), "max_no_layers": obj.get("max_no_layers")})
        return _obj
