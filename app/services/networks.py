from typing import ClassVar, Tuple, List
from typing import Optional

from fastapi import HTTPException
from pydantic import Field, StrictStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from typing_extensions import Annotated

from app.database.tables.network import Network as NetworkTable
from app.models.info import Info
from app.models.network import Network as Network


class NetworksService:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        NetworksService.subclasses += (cls,)

    async def create_network(self, network_input: Annotated[
        Optional[Network], Field(description="Network object that needs to be added to the store")],
                             db: AsyncSession) -> NetworkTable:
        """Upload a new network (Super User access required)."""
        db_network = NetworkTable(**network_input.model_dump())
        db.add(db_network)
        await db.commit()
        await db.refresh(db_network)
        return Network.model_validate(db_network)

    async def update_network(self, id: str, network_input: Annotated[
        Optional[Network], Field(description="Network object that needs to be added to the store")],
                             db: AsyncSession) -> NetworkTable:
        """Upload a new network (Super User access required)."""
        db_network = await self.get_network(id, db)
        for key, value in network_input.model_dump(by_alias=False).items():
            setattr(db_network, key, value)
        await db.commit()
        await db.refresh(db_network)
        return Network.model_validate(db_network)

    async def delete_network(self, id: StrictStr, db: AsyncSession) -> Info:
        """Delete a specific network by ID (Super User access required)."""
        db_network = await self.get_network(id, db)
        await db.delete(db_network)
        await db.commit()
        return Info(message="Network deleted successfully")

    async def get_network(self, id: StrictStr, db: AsyncSession) -> NetworkTable:
        """Fetch a specific network by ID."""
        result = await db.execute(select(NetworkTable).where(NetworkTable.network_profile_id == id))
        if (response := result.scalars().first()) is not None:
            return response
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Network not found")

    async def get_networks(self, db: AsyncSession) -> List[NetworkTable]:
        """Fetch a list of all networks."""
        result = await db.execute(select(NetworkTable))
        return [Network.model_validate(n) for n in result.scalars().all()]
