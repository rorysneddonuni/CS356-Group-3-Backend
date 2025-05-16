from typing import List, Optional, Tuple, Union

from fastapi import APIRouter, Body, Form, HTTPException, Path
from pydantic import Field, StrictBytes, StrictStr
from typing_extensions import Annotated

from app.models.error import Error
from app.models.experiment import Experiment
from app.models.experiment_input import ExperimentInput
from app.models.experiment_status import ExperimentStatus
from app.services.experiments import ExperimentsService

router = APIRouter()


@router.post("/experiments", responses={200: {"model": Experiment, "description": "Successful operation"},
                                        400: {"description": "Invalid input"},
                                        422: {"description": "Validation exception"},
                                        200: {"model": Error, "description": "Unexpected error"}, },
             tags=["experiments"], summary="Create a new experiment.", response_model_by_alias=True, )
async def create_experiment(experiment_input: Annotated[
    Optional[ExperimentInput], Field(description="Experiment object that needs to be added to the store")] = Body(None,
                                                                                                                  description="Experiment object that needs to be added to the store"), ) -> Experiment:
    """Create a new experiment under a given user."""
    return await ExperimentsService.subclasses[0]().create_experiment(experiment_input)


@router.delete("/experiments/{experimentId}",
               responses={200: {"description": "Experiment deleted"}, 400: {"description": "Invalid experiment value"},
                          200: {"model": Error, "description": "Unexpected error"}, }, tags=["experiments"],
               summary="Delete an experiment.", response_model_by_alias=True, )
async def delete_experiment(
        experiment_id: Annotated[StrictStr, Field(description="ID to uniquely identify an experiment.")] = Path(...,
                                                                                                                description="ID to uniquely identify an experiment."), ) -> None:
    """Delete an experiment."""
    return await ExperimentsService.subclasses[0]().delete_experiment(experiment_id)


@router.get("/experiments/{experimentId}", responses={200: {"model": Experiment, "description": "Successful operation"},
                                                      400: {"description": "Invalid status value"},
                                                      200: {"model": Error, "description": "Unexpected error"}, },
            tags=["experiments"], summary="Get experiment by ID.", response_model_by_alias=True, )
async def get_experiment(
        experiment_id: Annotated[StrictStr, Field(description="ID to uniquely identify an experiment.")] = Path(...,
                                                                                                                description="ID to uniquely identify an experiment."), ) -> Experiment:
    """Get full details of an experiment by its unique ID."""
    return await ExperimentsService.subclasses[0]().get_experiment(experiment_id)


@router.get("/experiments/{experimentId}/status",
            responses={200: {"model": ExperimentStatus, "description": "Experiment status retrieved successfully."},
                       404: {"model": Error, "description": "Experiment not found."},
                       200: {"model": Error, "description": "Unexpected error while retrieving experiment status."}, },
            tags=["experiments"], summary="Get experiment status", response_model_by_alias=True, )
async def get_experiment_status(
        experiment_id: Annotated[StrictStr, Field(description="Unique ID to identify the experiment.")] = Path(...,
                                                                                                               description="Unique ID to identify the experiment."), ) -> ExperimentStatus:
    """Retrieve the current status and progress of an experiment."""
    return await ExperimentsService.subclasses[0]().get_experiment_status(experiment_id)


@router.get("/experiments", responses={200: {"model": Experiment, "description": "Successful operation"},
                                       400: {"description": "Invalid request"},
                                       422: {"description": "Validation exception"},
                                       200: {"model": Error, "description": "Unexpected error"}, },
            tags=["experiments"], summary="List experiments.", response_model_by_alias=True, )
async def get_experiments() -> Experiment:
    """List experiments for a given user."""
    return await ExperimentsService.subclasses[0]().get_experiments()


@router.put("/experiments/{experimentId}",
            responses={200: {"description": "successful operation"}, 400: {"description": "bad request"},
                       404: {"description": "experiment not found"},
                       200: {"model": Error, "description": "Unexpected error"}, }, tags=["experiments"],
            summary="Update an experiment.", response_model_by_alias=True, )
async def update_experiment(
        experiment_id: Annotated[StrictStr, Field(description="ID to uniquely identify an experiment.")] = Path(...,
                                                                                                                description="ID to uniquely identify an experiment."),
        experiment_input: Annotated[Optional[ExperimentInput], Field(
            description="Experiment object that needs to be added to the store")] = Body(None,
                                                                                         description="Experiment object that needs to be added to the store"), ) -> None:
    """This can only be done by the user who owns the experiment."""
    return await ExperimentsService.subclasses[0]().update_experiment(experiment_id, experiment_input)
