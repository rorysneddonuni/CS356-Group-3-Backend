from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import ClassVar, List, Optional

from pydantic import BaseModel, Field, StrictStr

from app.models.experiment_sequence import ExperimentSequence, ExperimentSequenceInput

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
    experiment_name: StrictStr = Field(alias="ExperimentName")
    description: Optional[StrictStr] = Field(alias="Description")
    sequences: List[ExperimentSequenceInput] = Field(alias="Sequences")
    status: Optional[ExperimentStatus] = Field(alias="Status", default=None)

    __properties: ClassVar[List[str]] = ["ExperimentName", "Description", "Sequences", "Status"]
    model_config = {
        "populate_by_name": True,
        "validate_assignment": True,
        "protected_namespaces": (),
        "from_attributes": True
    }


class Experiment(ExperimentInput):
    """
    Experiment
    """  # noqa: E501
    id: Optional[int] = Field(alias="Id")
    created_at: Optional[datetime] = Field(default=None, alias="CreatedAt")
    owner_id: int = Field(alias="OwnerId")
    status: Optional[ExperimentStatus] = Field(alias="Status", default=ExperimentStatus.PENDING)
    sequences: List[ExperimentSequence] = Field(alias="Sequences")

    __properties: ClassVar[List[str]] = ["Id", "ExperimentName", "Description", "Sequences", "CreatedAt", "OwnerId",
                                         "Status", "Sequences"]
    model_config = {"populate_by_name": True, "validate_assignment": True, "protected_namespaces": (),
                    "from_attributes": True}
