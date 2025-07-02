from typing import List, Optional

from fastapi import APIRouter, Body, Path, Depends
from pydantic import Field, StrictStr
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse
from typing_extensions import Annotated

from app.auth.dependencies import require_minimum_role, super_admin_dependency, user_dependency
from app.database.database import get_db
from app.models.encoder import Encoder
from app.models.encoder_input import EncoderInput
from app.models.error import Error
from app.models.user import User
from app.services.encoders import EncodersService

router = APIRouter()


@router.post("/infrastructure/encoders", responses={200: {"description": "Encoder created"},
                                                    400: {"model": Error, "description": "Encoder already exists"},
                                                    422: {"description": "Validation exception"}}, tags=["encoders"],
             summary="Create encoder", response_model_by_alias=True, )
async def create_encoder(encoder_input: Annotated[
    Optional[EncoderInput], Field(description="Encoder object to be added to the store")] = Body(None,
                                                                                                 description="Encoder object to be added to the store"),
                         db: AsyncSession = Depends(get_db),
                         current_user: User = Depends(super_admin_dependency)) -> JSONResponse:
    """Create a new encoder (Super User access required)."""
    return await EncodersService().create_encoder(encoder_input, db)


@router.delete("/infrastructure/encoders/{id}", responses={200: {"model": Encoder, "description": "Encoder deleted"},
                                                           404: {"model": Error, "description": "Encoder not found"}},
               tags=["encoders"], summary="Delete encoder", response_model_by_alias=True)
async def delete_encoder(id: StrictStr = Path(..., description=""), db: AsyncSession = Depends(get_db),
                         current_user: User = Depends(super_admin_dependency)) -> JSONResponse:
    """Delete a specific encoder (Super User access required)."""
    return await EncodersService().delete_encoder(id, db)


@router.get("/infrastructure/encoders/{id}", responses={200: {"model": Encoder, "description": "Encoder details"},
                                                        404: {"model": Error, "description": "Encoder not found"}, },
            tags=["encoders"], summary="Retrieve encoder", response_model_by_alias=True, )
async def get_encoder(id: StrictStr = Path(..., description=""), db: AsyncSession = Depends(get_db),
                      current_user: User = Depends(user_dependency)) -> Encoder:
    """Fetch a specific encoder by ID."""
    return await EncodersService().get_encoder(id, db)


@router.get("/infrastructure/encoders", responses={200: {"model": List[Encoder], "description": "A list of encoders"},
                                                   404: {"model": Error, "description": "No encoders found"}},
            tags=["encoders"], summary="Retrieve encoder list", response_model_by_alias=True, )
async def get_encoders(db: AsyncSession = Depends(get_db),
                       current_user: User = Depends(user_dependency)) -> List[Encoder]:
    """Fetch a list of all encoders."""
    return await EncodersService().get_encoders(db)


@router.put("/infrastructure/encoders/{id}",
            responses={200: {"description": "Encoder updated"}, 400: {"model": Error, "description": "Invalid payload"},
                       404: {"model": Error, "description": "Encoder not found"},
                       422: {"description": "Validation exception"}}, tags=["encoders"], summary="Update encoder",
            response_model_by_alias=True, )
async def update_encoder(id: StrictStr = Path(..., description=""), db: AsyncSession = Depends(get_db),
                         current_user: User = Depends(super_admin_dependency), encoder_input: Annotated[
            Optional[EncoderInput], Field(description="Encoder object to be added to the store")] = Body(None,
                                                                                                         description="Encoder object to be added to the store"), ) -> JSONResponse:
    """Update an existing encoder (Super User access required)."""
    return await EncodersService().update_encoder(id, db, encoder_input)
