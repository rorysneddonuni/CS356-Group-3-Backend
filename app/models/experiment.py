from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import ClassVar, List, Optional

from pydantic import BaseModel, Field, StrictStr

from app.models.experiment_sequence import ExperimentSequence

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
    sequences: List[ExperimentSequence] = Field(alias="sequences")

    __properties: ClassVar[List[str]] = ["experimentName", "description", "sequences"]
    model_config = {"populate_by_name": True, "validate_assignment": True, "protected_namespaces": (),
                    "from_attributes": True}


class Experiment(ExperimentInput):
    """
    Experiment
    """  # noqa: E501
    id: Optional[int] = Field(alias="id")
    created_at: Optional[datetime] = Field(default=None, alias="createdAt")
    owner_id: int = Field(alias="ownerId")
    status: Optional[ExperimentStatus] = Field(alias="status", default=ExperimentStatus.PENDING)
    sequences: List[ExperimentSequence] = Field(alias="sequences")

    __properties: ClassVar[List[str]] = ["id", "experimentName", "description", "sequences", "createdAt", "ownerId",
                                         "status", "sequences"]
    model_config = {"populate_by_name": True, "validate_assignment": True, "protected_namespaces": (),
                    "from_attributes": True}
