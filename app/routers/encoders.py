from typing import List, Optional

from fastapi import APIRouter, Body, HTTPException, Path
from fastapi.params import Depends
from pydantic import Field, StrictInt
from typing_extensions import Annotated

from app.auth.dependencies import require_minimum_role
from app.models.encoder import Encoder
from app.models.encoder_input import EncoderInput
from app.models.error import Error
from app.models.user import User
from app.services.encoders import EncodersService

router = APIRouter()


@router.post("/infrastructure/encoders", responses={200: {"description": "Encoder created"},
                                                    400: {"model": Error, "description": "Invalid payload"},
                                                    200: {"model": Error, "description": "Unexpected error"}, },
             tags=["encoders"], summary="Create encoder", response_model_by_alias=True, )
async def create_encoder(current_user: User = Depends(require_minimum_role("super_admin")),
        encoder_input: Annotated[
    Optional[EncoderInput],
    Field(description="Encoder object to be added to the store")] =
        Body(None,description="Encoder object to be added to the store"), ) -> None:
    """Create a new encoder (Super User access required)."""
    if not EncodersService.subclasses:
        raise HTTPException(status_code=501, detail="Not implemented")
    return await EncodersService.subclasses[0]().create_encoder(encoder_input)


@router.delete("/infrastructure/encoders/{id}",
               responses={ 200: {"model": Encoder, "description": "Encoder deleted"},
                           404: {"model": Error, "description": "Encoder not found"},
                           200: {"model": Error, "description": "Unexpected error"}, },
               tags=["encoders"], summary="Delete encoder", response_model_by_alias=True, )
async def delete_encoder(id: StrictInt = Path(..., description=""),
                         current_user: User = Depends(require_minimum_role("super_admin")),) -> Encoder:
    """Delete a specific encoder (Super User access required)."""
    if not EncodersService.subclasses:
        raise HTTPException(status_code=501, detail="Not implemented")
    return await EncodersService.subclasses[0]().delete_encoder(id)


@router.get("/infrastructure/encoders/{id}", responses={200: {"model": Encoder, "description": "Encoder details"},
                                                        404: {"model": Error, "description": "Encoder not found"},
                                                        200: {"model": Error, "description": "Unexpected error"}, },
            tags=["encoders"], summary="Retrieve encoder", response_model_by_alias=True, )
async def get_encoder(id: StrictInt = Path(..., description=""),
                      current_user: User = Depends(require_minimum_role("user")),) -> Encoder:
    """Fetch a specific encoder by ID."""
    if not EncodersService.subclasses:
        raise HTTPException(status_code=501, detail="Not implemented")
    return await EncodersService.subclasses[0]().get_encoder(id)


@router.get("/infrastructure/encoders", responses={200: {"model": List[Encoder], "description": "A list of encoders"},
                                                   200: {"model": Error, "description": "Unexpected error"}, },
            tags=["encoders"], summary="Retrieve encoder list", response_model_by_alias=True, )
async def get_encoders(current_user: User = Depends(require_minimum_role("user")),) -> List[Encoder]:
    """Fetch a list of all encoders."""
    if not EncodersService.subclasses:
        raise HTTPException(status_code=501, detail="Not implemented")
    return await EncodersService.subclasses[0]().get_encoders()


@router.put("/infrastructure/encoders/{id}",
            responses={200: {"description": "Encoder updated"}, 400: {"model": Error, "description": "Invalid payload"},
                       404: {"model": Error, "description": "Encoder not found"},
                       200: {"model": Error, "description": "Unexpected error"}, }, tags=["encoders"],
            summary="Update encoder", response_model_by_alias=True, )
async def update_encoder(id: StrictInt = Path(..., description=""),
                         current_user: User = Depends(require_minimum_role("super_admin")), encoder_input: Annotated[
    Optional[EncoderInput], Field(description="Encoder object to be added to the store")] = Body(None,
                                                                                                 description="Encoder object to be added to the store"), ) -> None:
    """Update an existing encoder (Super User access required)."""
    if not EncodersService.subclasses:
        raise HTTPException(status_code=501, detail="Not implemented")
    return await EncodersService.subclasses[0]().update_encoder(id, encoder_input)
