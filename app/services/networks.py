from typing import List
from fastapi import HTTPException
from pydantic import Field, StrictStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from typing_extensions import Annotated

from app.database.tables.network import Network as NetworkTable
from app.models.info import Info
from app.models.network import Network, NetworkInput


class NetworksService:

    async def create_network(
        self,
        network_input: Annotated[NetworkInput, Field(description="Network object that needs to be added")],
        db: AsyncSession
    ) -> Network:
        db_network = NetworkTable(**network_input.model_dump(by_alias=False))
        db.add(db_network)
        await db.commit()
        await db.refresh(db_network)
        return Network.model_validate(db_network, from_attributes=True)

    async def update_network(
        self,
        id: StrictStr,
        network_input: Annotated[NetworkInput, Field(description="Network object to update")],
        db: AsyncSession
    ) -> Network:
        db_network = await self._get_db_network(id, db)
        for key, value in network_input.model_dump(by_alias=False).items():
            setattr(db_network, key, value)
        await db.commit()
        await db.refresh(db_network)
        return Network.model_validate(db_network, from_attributes=True)

    async def delete_network(self, id: StrictStr, db: AsyncSession) -> Info:
        db_network = await self._get_db_network(id, db)
        await db.delete(db_network)
        await db.commit()
        return Info(message="Network deleted successfully")

    async def get_network(self, id: StrictStr, db: AsyncSession) -> Network:
        db_network = await self._get_db_network(id, db)
        return Network.model_validate(db_network, from_attributes=True)

    async def get_networks(self, db: AsyncSession) -> List[Network]:
        result = await db.execute(select(NetworkTable))
        return [Network.model_validate(n, from_attributes=True) for n in result.scalars().all()]

    async def _get_db_network(self, id: StrictStr, db: AsyncSession) -> NetworkTable:
        result = await db.execute(select(NetworkTable).where(NetworkTable.network_profile_id == int(id)))
        db_network = result.scalars().first()
        if not db_network:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Network not found")
        return db_network
