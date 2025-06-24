from typing import Optional, List

from fastapi import APIRouter
from fastapi import Body
from fastapi.params import Depends, Path
from pydantic import Field, StrictStr
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse
from typing_extensions import Annotated

from app.auth.dependencies import require_minimum_role
from app.database.database import get_db
from app.models.experiment import Experiment, ExperimentInput
from app.models.user import User
from app.services.experiments import ExperimentsService

router = APIRouter()


@router.post("/experiments", responses={200: {"model": Experiment, "description": "Successful operation"},
                                        400: {"description": "Invalid input"},
                                        422: {"description": "Validation exception"}}, tags=["experiments"],
             summary="Create a new experiment.", response_model_by_alias=True, )
async def create_experiment(current_user: User = Depends(require_minimum_role("user")), experiment_input: Annotated[
    Optional[ExperimentInput], Field(description="Experiment object that needs to be added to the store")] = Body(None,
                                                                                                                  description="Experiment object that needs to be added to the store"),
                            db: AsyncSession = Depends(get_db)) -> Experiment:
    """Create a new experiment under a given user."""
    return await ExperimentsService().create_experiment(current_user.id, experiment_input, db)


@router.delete("/experiments/{experiment_id}",
               responses={200: {"description": "Experiment deleted"}, 400: {"description": "Invalid experiment value"}},
               tags=["experiments"], summary="Delete an experiment.", response_model_by_alias=True, )
async def delete_experiment(current_user: User = Depends(require_minimum_role("admin")), experiment_id: Annotated[
    StrictStr, Field(description="ID to uniquely identify an experiment.")] = Path(...,
                                                                                   description="ID to uniquely identify an experiment."),
                            db: AsyncSession = Depends(get_db)) -> JSONResponse:
    """Delete an experiment."""
    return await ExperimentsService().delete_experiment(experiment_id, db)


@router.get("/experiments/{experiment_id}",
            responses={200: {"model": Experiment, "description": "Successful operation"},
                       404: {"description": "Experiment not found"}}, tags=["experiments"],
            summary="Get experiment by ID.", response_model_by_alias=True, )
async def get_experiment(current_user: User = Depends(require_minimum_role("user")), experiment_id: Annotated[
    StrictStr, Field(description="ID to uniquely identify an experiment.")] = Path(...,
                                                                                   description="ID to uniquely identify an experiment."),
                         db: AsyncSession = Depends(get_db)) -> Experiment:
    """Get full details of an experiment by its unique ID."""
    return await ExperimentsService().get_experiment(experiment_id, db)


@router.get(
    "/experiments",
    responses={
        200: {"model": List[Experiment], "description": "Successful operation"},
        404: {"description": "No experiments found for user"},
        422: {"description": "Validation exception"},
    },
    tags=["experiments"],
    summary="List experiments.",
    response_model_by_alias=True,
    response_model=List[Experiment],
)
async def get_experiments(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_minimum_role("user")),
) -> List[Experiment]:
    """List experiments for a given user."""
    
    if current_user.role == "user":
        return await ExperimentsService().get_experiments(current_user.id, db)
    return await ExperimentsService().get_all_experiments(db)


@router.put("/experiments/{experiment_id}", responses={200: {"description": "successful operation"}, 400: {
    "description": "Only the owner of the experiment can update the experiment"},
                                                       404: {"description": "experiment not found"},
                                                       422: {"description": "Validation exception"}},
            tags=["experiments"], summary="Update an experiment.", response_model_by_alias=True, )
async def update_experiment(current_user: User = Depends(require_minimum_role("user")), experiment_id: Annotated[
    StrictStr, Field(description="ID to uniquely identify an experiment.")] = Path(...,
                                                                                   description="ID to uniquely identify an experiment."),
                            experiment_input: Annotated[Optional[ExperimentInput], Field(
                                description="Experiment object that needs to be added to the store")] = Body(None,
                                                                                                             description="Experiment object that needs to be added to the store"),
                            db: AsyncSession = Depends(get_db)) -> Experiment:
    """This can only be done by the user who owns the experiment."""
    return await ExperimentsService().update_experiment(current_user.id, experiment_id, experiment_input, db)
