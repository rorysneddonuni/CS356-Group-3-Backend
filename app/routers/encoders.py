# app/routers/encoders.py

from typing import List, Optional

from fastapi import APIRouter, Body, HTTPException, Path, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import StrictInt
from typing_extensions import Annotated

from app.database.database import get_db
from app.models.encoder import Encoder
from app.models.encoder_input import EncoderInput
from app.models.error import Error
from app.services.encoders import EncodersService

router = APIRouter()


@router.post(
    "/infrastructure/encoders",
    response_model=Encoder,
    responses={
        200: {"description": "Encoder created"},
        400: {"model": Error, "description": "Invalid payload"},
        500: {"model": Error, "description": "Unexpected error"},
    },
    tags=["encoders"],
    summary="Create encoder",
    response_model_by_alias=True,
)
async def create_encoder(
    encoder_input: Annotated[
        Optional[EncoderInput],
        Body(description="Encoder object to be added to the store")
    ] = None,
    db: AsyncSession = Depends(get_db),
) -> Encoder:
    if not EncodersService.subclasses:
        raise HTTPException(status_code=501, detail="Not implemented")
    return await EncodersService.subclasses[0]().create_encoder(encoder_input, db)


@router.get(
    "/infrastructure/encoders",
    response_model=List[Encoder],
    responses={
        200: {"model": List[Encoder], "description": "A list of encoders"},
        500: {"model": Error, "description": "Unexpected error"},
    },
    tags=["encoders"],
    summary="Retrieve encoder list",
    response_model_by_alias=True,
)
async def get_encoders(
    db: AsyncSession = Depends(get_db),
) -> List[Encoder]:
    if not EncodersService.subclasses:
        raise HTTPException(status_code=501, detail="Not implemented")
    return await EncodersService.subclasses[0]().get_encoders(db)


@router.get(
    "/infrastructure/encoders/{id}",
    response_model=Encoder,
    responses={
        200: {"model": Encoder, "description": "Encoder details"},
        404: {"model": Error, "description": "Encoder not found"},
        500: {"model": Error, "description": "Unexpected error"},
    },
    tags=["encoders"],
    summary="Retrieve encoder",
    response_model_by_alias=True,
)
async def get_encoder(
    id: Annotated[StrictInt, Path(..., description="The encoder ID to fetch")],
    db: AsyncSession = Depends(get_db),
) -> Encoder:
    if not EncodersService.subclasses:
        raise HTTPException(status_code=501, detail="Not implemented")
    return await EncodersService.subclasses[0]().get_encoder(id, db)


@router.put(
    "/infrastructure/encoders/{id}",
    response_model=Encoder,
    responses={
        200: {"model": Encoder, "description": "Encoder updated"},
        400: {"model": Error, "description": "Invalid payload"},
        404: {"model": Error, "description": "Encoder not found"},
        500: {"model": Error, "description": "Unexpected error"},
    },
    tags=["encoders"],
    summary="Update encoder",
    response_model_by_alias=True,
)
async def update_encoder(
    id: Annotated[StrictInt, Path(..., description="The encoder ID to update")],
    encoder_input: Annotated[
        Optional[EncoderInput],
        Body(description="Encoder object to be updated")
    ] = None,
    db: AsyncSession = Depends(get_db),
) -> Encoder:
    if not EncodersService.subclasses:
        raise HTTPException(status_code=501, detail="Not implemented")
    return await EncodersService.subclasses[0]().update_encoder(id, encoder_input, db)


@router.delete(
    "/infrastructure/encoders/{id}",
    status_code=204,
    responses={
        204: {"description": "Encoder deleted"},
        404: {"model": Error, "description": "Encoder not found"},
        500: {"model": Error, "description": "Unexpected error"},
    },
    tags=["encoders"],
    summary="Delete encoder",
    response_model_by_alias=True,
)
async def delete_encoder(
    id: Annotated[StrictInt, Path(..., description="The encoder ID to delete")],
    db: AsyncSession = Depends(get_db),
) -> None:
    if not EncodersService.subclasses:
        raise HTTPException(status_code=501, detail="Not implemented")
    await EncodersService.subclasses[0]().delete_encoder(id, db)
