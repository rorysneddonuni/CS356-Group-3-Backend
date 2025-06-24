from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.params import File, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import StreamingResponse

from app.auth.dependencies import require_minimum_role
from app.config.settings import Settings
from app.config.settings import get_settings
from app.database.database import get_db
from app.models.info import Info
from app.models.user import User
from app.services.results import ResultsService

router = APIRouter(prefix="/experiments")


@router.get("/{experiment_id}/results",
            responses={200: {"description": "Successful operation"}, 400: {"description": "Invalid status value"}},
            tags=["experiments", "results"], summary="Get results for an experiment.", response_model_by_alias=True, )
async def get_experiment_results(current_user: User = Depends(require_minimum_role("user")),
                                 experiment_id: int = Path(..., description="ID to uniquely identify an experiment."),
                                 db: AsyncSession = Depends(get_db)) -> StreamingResponse:
    """Get list of files to download for results."""
    if not ResultsService.subclasses:
        raise HTTPException(status_code=501, detail="Not implemented")
    return await ResultsService.subclasses[0]().get_experiment_results(experiment_id, current_user, db)


@router.post("/{experiment_id}/results",
             responses={200: {"description": "Successful operation"}, 422: {"description": "Validation exception"}},
             tags=["experiments", "results"], summary="Upload results for an experiment.",
             response_model_by_alias=True, )
async def upload_results(current_user: User = Depends(require_minimum_role("user")),
                         experiment_id: int = Path(..., description="ID to uniquely identify an experiment."),
                         file: UploadFile = File(...), db: AsyncSession = Depends(get_db),
                         settings: Settings = Depends(get_settings)) -> Info:
    """This can only be done by the logged-in user."""
    if not ResultsService.subclasses:
        raise HTTPException(status_code=501, detail="Not implemented")
    return await ResultsService.subclasses[0]().upload_result(experiment_id, file, db, settings)
