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
    description: StrictStr = Field(alias="Description")
    status: ExperimentStatus = ExperimentStatus.PENDING
    sequences: List[ExperimentSequenceInput] = Field(alias="Sequences")

    __properties: ClassVar[List[str]] = ["ExperimentName", "Description", "Sequences", "Status"]
    model_config = {"populate_by_name": True, "validate_assignment": True, "protected_namespaces": (),
                    "from_attributes": True}


class ExperimentUpdateInput(BaseModel):
    experiment_name: Optional[str] = Field(None, alias="ExperimentName")
    description: Optional[str] = Field(None, alias="Description")
    status: Optional[ExperimentStatus] = Field(None, alias="Status")
    add_sequences: List[ExperimentSequenceInput] = Field(default_factory=list, alias="AddSequences")
    remove_sequence_ids: List[int] = Field(default_factory=list, alias="RemoveSequenceIds")

    model_config = {
        "populate_by_name": True,
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
    sequences: List[ExperimentSequence] = Field(alias="Sequences")

    __properties: ClassVar[List[str]] = ["Id", "ExperimentName", "Description", "Sequences", "CreatedAt", "OwnerId",
                                         "Status", "Sequences"]
    model_config = {"populate_by_name": True, "validate_assignment": True, "protected_namespaces": (),
                    "from_attributes": True}
