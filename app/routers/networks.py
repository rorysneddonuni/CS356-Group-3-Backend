from typing import List, Optional

from fastapi import APIRouter, Body, Path, Depends
from pydantic import Field, StrictStr
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated

from app.auth.dependencies import require_minimum_role
from app.database.database import get_db
from app.models.error import Error
from app.models.info import Info
from app.models.network import Network, NetworkInput
from app.models.user import User
from app.services.networks import NetworksService

router = APIRouter()


@router.post("/infrastructure/networks", responses={201: {"description": "Network created"},
                                                    400: {"model": Error, "description": "Invalid payload"},
                                                    422: {"description": "Validation exception"}}, tags=["networks"],
             summary="Create network", response_model_by_alias=True, )
async def create_network(current_user: User = Depends(require_minimum_role("user")), network_input: Annotated[
    Optional[NetworkInput], Field(description="Network object that needs to be added to the store")] = Body(None,
                                                                                                            description="Network object that needs to be added to the store"),
                         db: AsyncSession = Depends(get_db)) -> Network:
    """Upload a new network (Super User access required)."""
    return await NetworksService().create_network(network_input, db)


@router.put("/infrastructure/networks/{network_id}", responses={200: {"description": "Network updated"},
                                                                404: {"model": Error,
                                                                      "description": "Network not found"},
                                                                422: {"description": "Validation exception"}},
            tags=["networks"], summary="Create network", response_model_by_alias=True, )
async def update_network(current_user: User = Depends(require_minimum_role("super_admin")),
                         network_id: StrictStr = Path(..., description=""), network_input: Annotated[
            Optional[NetworkInput], Field(description="Network object that needs to be updated")] = Body(None,
                                                                                                         description="Network object that needs to be updated"),
                         db: AsyncSession = Depends(get_db)) -> Network:
    """Upload a new network (Super User access required)."""
    return await NetworksService().update_network(network_id, network_input, db)


@router.delete("/infrastructure/networks/{id}", responses={200: {"model": Network, "description": "Network deleted"},
                                                           404: {"model": Error, "description": "Network not found"}},
               tags=["networks"], summary="Delete network", response_model_by_alias=True, )
async def delete_network(current_user: User = Depends(require_minimum_role("super_admin")),
                         id: StrictStr = Path(..., description=""), db: AsyncSession = Depends(get_db)) -> Info:
    """Delete a specific network by ID (Super User access required)."""
    return await NetworksService().delete_network(id, db)


@router.get("/infrastructure/networks/{id}", responses={200: {"model": Network, "description": "Network details"},
                                                        404: {"model": Error, "description": "Network not found"}},
            tags=["networks"], summary="Retrieve network", response_model_by_alias=True, )
async def get_network(current_user: User = Depends(require_minimum_role("user")),
                      id: StrictStr = Path(..., description=""), db: AsyncSession = Depends(get_db)) -> Network:
    """Fetch a specific network by ID."""
    return await NetworksService().get_network(id, db)


@router.get("/infrastructure/networks", responses={200: {"model": List[Network], "description": "A list of networks"}},
            tags=["networks"], summary="Retrieve networks list", response_model_by_alias=True, )
async def get_networks(current_user: User = Depends(require_minimum_role("user")),
                       db: AsyncSession = Depends(get_db)) -> List[Network]:
    """Fetch a list of all networks."""
    return await NetworksService().get_networks(db)
