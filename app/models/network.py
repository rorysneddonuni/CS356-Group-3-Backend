from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic import BaseModel, Field, StrictInt, StrictStr

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self


class NetworkInput(BaseModel):
    name: Optional[StrictStr] = Field(None, alias="name")
    packet_loss: Optional[StrictInt] = Field(default=None, alias="packetLoss")
    delay: Optional[StrictInt] = Field(default=None, alias="delay")
    jitter: Optional[StrictInt] = Field(default=None, alias="jitter")
    bandwidth: Optional[StrictInt] = Field(default=None, alias="bandwidth")

    __properties: ClassVar[List[str]] = ["name", "packet_loss", "delay", "jitter", "bandwidth"]
    model_config = {"populate_by_name": True, "validate_assignment": True, "protected_namespaces": (),
                    "from_attributes": True}


class Network(BaseModel):
    """
    Network
    """  # noqa: E501
    id: Optional[StrictInt] = Field(default=None)

    __properties: ClassVar[List[str]] = ["id", "name", "packet_loss", "delay", "jitter", "bandwidth"]
    model_config = {"populate_by_name": True, "validate_assignment": True, "protected_namespaces": (),
                    "from_attributes": True}
