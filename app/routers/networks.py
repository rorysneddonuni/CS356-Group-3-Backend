from typing import List, Optional

from fastapi import APIRouter, Body, HTTPException, Path, Depends
from pydantic import Field, StrictStr
from typing_extensions import Annotated

from app.auth.dependencies import require_minimum_role
from app.models.error import Error
from app.models.network import Network
from app.models.network_input import NetworkInput
from app.models.user import User
from app.services.networks import NetworksService

router = APIRouter()


@router.post("/infrastructure/networks", responses={200: {"description": "Network created"},
                                                    400: {"model": Error, "description": "Invalid payload"},
                                                    422: {"description": "Validation exception"}}, tags=["networks"],
             summary="Create network", response_model_by_alias=True, )
async def create_network(current_user: User = Depends(require_minimum_role("super_admin")), network_input: Annotated[
    Optional[NetworkInput], Field(description="Network object that needs to be added to the store")] = Body(None,
                                                                                                            description="Network object that needs to be added to the store"), ) -> None:
    """Upload a new network (Super User access required)."""
    if not NetworksService.subclasses:
        raise HTTPException(status_code=501, detail="Not implemented")
    return await NetworksService.subclasses[0]().create_network(network_input)


@router.delete("/infrastructure/networks/{id}", responses={200: {"model": Network, "description": "Network deleted"},
                                                           404: {"model": Error, "description": "Network not found"}},
               tags=["networks"], summary="Delete network", response_model_by_alias=True, )
async def delete_network(current_user: User = Depends(require_minimum_role("super_admin")),
                         id: StrictStr = Path(..., description=""), ) -> Network:
    """Delete a specific network by ID (Super User access required)."""
    if not NetworksService.subclasses:
        raise HTTPException(status_code=501, detail="Not implemented")
    return await NetworksService.subclasses[0]().delete_network(id)


@router.get("/infrastructure/networks/{id}", responses={200: {"model": Network, "description": "Network details"},
                                                        404: {"model": Error, "description": "Network not found"}},
            tags=["networks"], summary="Retrieve network", response_model_by_alias=True, )
async def get_network(current_user: User = Depends(require_minimum_role("user")),
                      id: StrictStr = Path(..., description=""), ) -> Network:
    """Fetch a specific network by ID."""
    if not NetworksService.subclasses:
        raise HTTPException(status_code=501, detail="Not implemented")
    return await NetworksService.subclasses[0]().get_network(id)


@router.get("/infrastructure/networks", responses={200: {"model": List[Network], "description": "A list of networks"}},
            tags=["networks"], summary="Retrieve networks list", response_model_by_alias=True, )
async def get_networks(current_user: User = Depends(require_minimum_role("user")), ) -> List[Network]:
    """Fetch a list of all networks."""
    if not NetworksService.subclasses:
        raise HTTPException(status_code=501, detail="Not implemented")
    return await NetworksService.subclasses[0]().get_networks()
