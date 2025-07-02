from typing import List, Optional

from fastapi import APIRouter, Body, Path, Depends
from pydantic import Field, StrictStr
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated

from app.auth.dependencies import require_minimum_role, user_dependency, super_admin_dependency
from app.database.database import get_db
from app.models.error import Error
from app.models.info import Info
from app.models.network import Network, NetworkInput
from app.models.user import User
from app.services.networks import NetworksService

router = APIRouter()

@router.post("/infrastructure/networks",
             status_code=201,
             responses={201: {"description": "Network created"},
                                                    400: {"model": Error, "description": "Invalid payload"},
                                                    422: {"description": "Validation exception"}},
             tags=["networks"], summary="Create network", response_model_by_alias=True)
async def create_network(
    current_user: User = Depends(user_dependency),
    network_input: Annotated[Optional[NetworkInput], Field(description="Network object that needs to be added to the store")] = Body(None),
    db: AsyncSession = Depends(get_db)
) -> Network:
    return await NetworksService().create_network(network_input, db)


@router.put("/infrastructure/networks/{network_id}", responses={200: {"description": "Network updated"},
                                                                404: {"model": Error, "description": "Network not found"},
                                                                422: {"description": "Validation exception"}},
            tags=["networks"], summary="Update network", response_model_by_alias=True)
async def update_network(
    current_user: User = Depends(super_admin_dependency),
    network_id: StrictStr = Path(..., description="Network ID"),
    network_input: Annotated[Optional[NetworkInput], Field(description="Network object that needs to be updated")] = Body(None),
    db: AsyncSession = Depends(get_db)
) -> Network:
    return await NetworksService().update_network(network_id, network_input, db)


@router.delete("/infrastructure/networks/{id}", responses={200: {"model": Network, "description": "Network deleted"},
                                                           404: {"model": Error, "description": "Network not found"}},
               tags=["networks"], summary="Delete network", response_model_by_alias=True)
async def delete_network(
    current_user: User = Depends(super_admin_dependency),
    id: StrictStr = Path(..., description="Network ID"),
    db: AsyncSession = Depends(get_db)
) -> Info:
    return await NetworksService().delete_network(id, db)


@router.get("/infrastructure/networks/{id}", responses={200: {"model": Network, "description": "Network details"},
                                                        404: {"model": Error, "description": "Network not found"}},
            tags=["networks"], summary="Retrieve network", response_model_by_alias=True)
async def get_network(
    current_user: User = Depends(user_dependency),
    id: StrictStr = Path(..., description="Network ID"),
    db: AsyncSession = Depends(get_db)
) -> Network:
    return await NetworksService().get_network(id, db)


@router.get("/infrastructure/networks", responses={200: {"model": List[Network], "description": "A list of networks"}},
            tags=["networks"], summary="Retrieve networks list", response_model_by_alias=True)
async def get_networks(
    current_user: User = Depends(user_dependency),
    db: AsyncSession = Depends(get_db)
) -> List[Network]:
    return await NetworksService().get_networks(db)
