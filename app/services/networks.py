from typing import ClassVar, Tuple
from typing import List, Optional

from pydantic import Field, StrictStr
from typing_extensions import Annotated

from app.models.network import Network
from app.models.network_input import NetworkInput


class NetworksService:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        NetworksService.subclasses = NetworksService.subclasses + (cls,)

    async def create_network(self, network_input: Annotated[
        Optional[NetworkInput], Field(description="Network object that needs to be added to the store")], ) -> None:
        """Upload a new network (Super User access required)."""
        ...

    async def delete_network(self, id: StrictStr, ) -> Network:
        """Delete a specific network by ID (Super User access required)."""
        ...

    async def get_network(self, id: StrictStr, ) -> Network:
        """Fetch a specific network by ID."""
        ...

    async def get_networks(self, ) -> List[Network]:
        """Fetch a list of all networks."""
        ...
