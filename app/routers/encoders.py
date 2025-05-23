from typing import List, Optional

from fastapi import APIRouter, Body, HTTPException, Path, Depends
from pydantic import Field, StrictInt
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse
from typing_extensions import Annotated

from app.database.database import get_db
from app.database.tables.encoders import Encoders
from app.models.encoder import Encoder
from app.models.encoder_input import EncoderInput
from app.models.error import Error
from app.services.encoders import EncodersService

router = APIRouter()


@router.post("/infrastructure/encoders", responses={200: {"description": "Encoder created"},
                                                    400: {"model": Error, "description": "Invalid payload"},
                                                    200: {"model": Error, "description": "Unexpected error"}, },
             tags=["encoders"], summary="Create encoder", response_model_by_alias=True, )
async def create_encoder(encoder_input: Annotated[
    Optional[EncoderInput], Field(description="Encoder object to be added to the store")] = Body(None,
                                                                                                 description="Encoder object to be added to the store"),
                         db: AsyncSession = Depends(get_db)) -> JSONResponse:
    """Create a new encoder (Super User access required)."""
    return await EncodersService().create_encoder(encoder_input, db)


@router.delete("/infrastructure/encoders/{id}", responses={200: {"model": Encoder, "description": "Encoder deleted"},
                                                           404: {"model": Error, "description": "Encoder not found"},
                                                           200: {"model": Error, "description": "Unexpected error"}, },
               tags=["encoders"], summary="Delete encoder", response_model_by_alias=True)
async def delete_encoder(id: StrictInt = Path(..., description=""), db: AsyncSession = Depends(get_db)) -> JSONResponse:
    """Delete a specific encoder (Super User access required)."""
    return await EncodersService().delete_encoder(id, db)


@router.get("/infrastructure/encoders/{id}", responses={200: {"model": Encoder, "description": "Encoder details"},
                                                        404: {"model": Error, "description": "Encoder not found"},
                                                        200: {"model": Error, "description": "Unexpected error"}, },
            tags=["encoders"], summary="Retrieve encoder", response_model_by_alias=True, )
async def get_encoder(id: StrictInt = Path(..., description=""), db: AsyncSession = Depends(get_db)) -> Encoder:
    """Fetch a specific encoder by ID."""
    return await EncodersService().get_encoder(id, db)


@router.get("/infrastructure/encoders", responses={200: {"model": List[Encoder], "description": "A list of encoders"},
                                                   200: {"model": Error, "description": "Unexpected error"}, },
            tags=["encoders"], summary="Retrieve encoder list", response_model_by_alias=True, )
async def get_encoders(db: AsyncSession = Depends(get_db)) -> List[Encoder]:
    """Fetch a list of all encoders."""
    return await EncodersService().get_encoders(db)


@router.put("/infrastructure/encoders/{id}",
            responses={200: {"description": "Encoder updated"}, 400: {"model": Error, "description": "Invalid payload"},
                       404: {"model": Error, "description": "Encoder not found"},
                       200: {"model": Error, "description": "Unexpected error"}, }, tags=["encoders"],
            summary="Update encoder", response_model_by_alias=True, )
async def update_encoder(id: StrictInt = Path(..., description=""), db: AsyncSession = Depends(get_db),
                         encoder_input: Annotated[
                             Optional[EncoderInput], Field(
                                 description="Encoder object to be added to the store")] = Body(None,
                                                                                                description="Encoder object to be added to the store"), ) -> None:
    """Update an existing encoder (Super User access required)."""
    return await EncodersService().update_encoder(id, db, encoder_input)
