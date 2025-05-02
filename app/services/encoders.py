from typing import ClassVar, Tuple
from typing import List, Optional

from pydantic import Field, StrictInt
from typing_extensions import Annotated

from app.models.encoder import Encoder
from app.models.encoder_input import EncoderInput


class EncodersService:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        EncodersService.subclasses = EncodersService.subclasses + (cls,)

    async def create_encoder(self, encoder_input: Annotated[
        Optional[EncoderInput], Field(description="Encoder object to be added to the store")], ) -> None:
        """Create a new encoder (Super User access required)."""
        ...

    async def delete_encoder(self, id: StrictInt, ) -> Encoder:
        """Delete a specific encoder (Super User access required)."""
        ...

    async def get_encoder(self, id: StrictInt, ) -> Encoder:
        """Fetch a specific encoder by ID."""
        ...

    async def get_encoders(self, ) -> List[Encoder]:
        """Fetch a list of all encoders."""
        ...

    async def update_encoder(self, id: StrictInt, encoder_input: Annotated[
        Optional[EncoderInput], Field(description="Encoder object to be added to the store")], ) -> None:
        """Update an existing encoder (Super User access required)."""
        ...
