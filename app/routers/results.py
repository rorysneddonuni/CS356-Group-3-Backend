from typing import List, Optional, Tuple, Union

from fastapi import APIRouter, Form, HTTPException, Path
from pydantic import Field, StrictBytes, StrictStr
from typing_extensions import Annotated

from app.models.error import Error
from app.services.results import ResultsService

router = APIRouter()


@router.get("/experiments/{experimentId}/results",
            responses={200: {"description": "Successful operation"}, 400: {"description": "Invalid status value"},
                       200: {"model": Error, "description": "Unexpected error"}, }, tags=["experiments", "results"],
            summary="Get results for an experiment.", response_model_by_alias=True, )
async def get_experiment_results(
        experiment_id: Annotated[StrictStr, Field(description="ID to uniquely identify an experiment.")] = Path(...,
                                                                                                                description="ID to uniquely identify an experiment."), ) -> None:
    """Get list of files to download for results."""
    if not ResultsService.subclasses:
        raise HTTPException(status_code=501, detail="Not implemented")
    return await ResultsService.subclasses[0]().get_experiment_results(experiment_id)


@router.post("/experiments/{experimentId}/results", responses={200: {"description": "Successful operation"},
                                                               200: {"model": Error,
                                                                     "description": "Unexpected error"}, },
             tags=["experiments", "results"], summary="Upload results for an experiment.",
             response_model_by_alias=True, )
async def upload_results(
        experiment_id: Annotated[StrictStr, Field(description="ID to uniquely identify an experiment.")] = Path(...,
                                                                                                                description="ID to uniquely identify an experiment."),
        filename: Optional[List[Union[StrictBytes, StrictStr, Tuple[StrictStr, StrictBytes]]]] = Form(None,
                                                                                                      description=""), ) -> None:
    """This can only be done by the logged-in user."""
    if not ResultsService.subclasses:
        raise HTTPException(status_code=501, detail="Not implemented")
    return await ResultsService.subclasses[0]().upload_results(experiment_id, filename)
