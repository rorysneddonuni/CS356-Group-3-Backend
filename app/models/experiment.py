from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import ClassVar, List, Optional

from pydantic import BaseModel, Field, StrictStr
from pydantic.v1 import StrictInt

from app.models.encoding_parameters import EncodingParameters
from app.models.network import Network

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self


class ExperimentStatus(str, Enum):
    COMPLETE = 'COMPLETE'
    PENDING = 'PENDING'
    ERROR = 'ERROR'


class ExperimentInput(BaseModel):
    """
    ExperimentInput
    """  # noqa: E501
    experiment_name: StrictStr = Field(alias="experimentName")
    description: Optional[StrictStr] = Field(alias="description")
    video_sources: List[StrictStr] = Field(alias="videoSources")
    encoding_parameters: EncodingParameters = Field(alias="encodingParameters")
    network_disruption_profile_id: int = Field(alias="networkDisruptionProfileId")
    metrics_requested: List[StrictStr] = Field(alias="metricsRequested")
    status: Optional[ExperimentStatus] = Field(alias="status", default=ExperimentStatus.PENDING)
    __properties: ClassVar[List[str]] = ["experimentName", "description", "videoSources", "encodingParameters",
                                         "networkDisruptionProfileId", "metricsRequested"]

    model_config = {"populate_by_name": True, "validate_assignment": True, "protected_namespaces": (), }


class Experiment(ExperimentInput):
    """
    Experiment
    """  # noqa: E501
    id: Optional[int] = Field(alias="id")
    created_at: Optional[datetime] = Field(default=None, alias="createdAt")
    network_disruption_profile: Network = Field(default=None, alias="networkDisruptionProfile")
    owner_id: int = Field(alias="ownerId")
    __properties: ClassVar[List[str]] = ["id", "experimentName", "description", "videoSources", "encodingParameters",
                                         "networkDisruptionProfileId", "metricsRequested", "status", "createdAt",
                                         "networkDisruptionProfile"]

    model_config = {"populate_by_name": True, "validate_assignment": True, "protected_namespaces": (), }
