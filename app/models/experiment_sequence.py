from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic import BaseModel, Field

from app.models.encoding_parameters import EncodingParameters
from app.models.network import Network

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self


class ExperimentSequenceInput(BaseModel):
    """
    ExperimentSequenceInput
    """  # noqa: E501
    network_topology_id: int = Field(alias="networkTopologyId")
    network_disruption_profile_id: int = Field(alias="networkDisruptionProfileId")
    # todo nuke this shit
    encoding_parameters: EncodingParameters = Field(alias="encodingParameters")

    __properties: ClassVar[List[str]] = ["networkTopologyId", "networkDisruptionProfileId", "encodingParameters"]
    model_config = {"populate_by_name": True, "validate_assignment": True, "protected_namespaces": (),
                    "from_attributes": True}


class ExperimentSequence(ExperimentSequenceInput):
    """
    ExperimentSequence
    """  # noqa: E501
    sequence_id: Optional[int] = Field(alias="sequenceId")
    network_topology: Network = Field(default=None, alias="networkTopologyId")
    network_disruption_profile: Network = Field(default=None, alias="networkDisruptionProfile")

    __properties: ClassVar[List[str]] = ["sequenceId", "networkTopologyId", "networkDisruptionProfileId",
                                         "encodingParameters", "networkDisruptionProfile", "networkTopology"]
    model_config = {"populate_by_name": True, "validate_assignment": True, "protected_namespaces": (),
                    "from_attributes": True}
