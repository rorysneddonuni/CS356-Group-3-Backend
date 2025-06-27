from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic import BaseModel, Field

from app.models.network import Network

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self


class ExperimentSequenceInput(BaseModel):
    network_topology_id: int = Field(alias="NetworkTopologyId")
    network_disruption_profile_id: int = Field(alias="NetworkDisruptionProfileId")
    encoding_parameters: dict = Field(alias="EncodingParameters")

    __properties: ClassVar[List[str]] = ["networkTopologyId", "networkDisruptionProfileId", "encodingParameters"]
    model_config = {"populate_by_name": True, "validate_assignment": True, "protected_namespaces": (),
                    "from_attributes": True}


class ExperimentSequence(ExperimentSequenceInput):
    """
    ExperimentSequence
    """  # noqa: E501
    sequence_id: int = Field(alias="SequenceId")
    network_topology: Optional[Network] = Field(default=None, alias="NetworkTopologyId")
    network_disruption_profile: Optional[Network] = Field(default=None, alias="NetworkDisruptionProfile")

    __properties: ClassVar[List[str]] = ["sequenceId", "networkTopologyId", "networkDisruptionProfileId",
                                         "encodingParameters", "networkDisruptionProfile", "networkTopology"]
    model_config = {"populate_by_name": True, "validate_assignment": True, "protected_namespaces": (),
                    "from_attributes": True}
