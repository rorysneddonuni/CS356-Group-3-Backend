from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic import BaseModel, Field, StrictInt, StrictStr


class NetworkInput(BaseModel):
    network_name: Optional[StrictStr] = Field(None, alias="networkName")
    description: Optional[StrictStr] = Field(None, alias="description")
    packet_loss: Optional[StrictInt] = Field(default=None, alias="packetLoss")
    delay: Optional[StrictInt] = Field(default=None, alias="delay")
    jitter: Optional[StrictInt] = Field(default=None, alias="jitter")
    bandwidth: Optional[StrictInt] = Field(default=None, alias="bandwidth")

    __properties: ClassVar[List[str]] = ["networkName", "description", "packetLoss", "delay", "jitter", "bandwidth"]
    model_config = {"populate_by_name": True, "validate_assignment": True, "protected_namespaces": (),
                    "from_attributes": True}


class Network(NetworkInput):
    """
    Network
    """  # noqa: E501
    network_profile_id: Optional[StrictInt] = Field(default=None)

    __properties: ClassVar[List[str]] = ["networkProfileId", "networkName", "description", "packetLoss", "delay", "jitter", "bandwidth"]
    model_config = {"populate_by_name": True, "validate_assignment": True, "protected_namespaces": (),
                    "from_attributes": True}
