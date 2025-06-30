import json
from typing import ClassVar, Tuple
from typing import List, Optional

from fastapi import HTTPException
from pydantic import Field, StrictInt
from sqlalchemy import select, or_
from starlette.responses import JSONResponse
from typing_extensions import Annotated

from app.database.tables.encoders import Encoders as encoder_table
from app.models.encoder import Encoder
from app.models.encoder_input import EncoderInput


class EncodersService:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        EncodersService.subclasses = EncodersService.subclasses + (cls,)

    async def create_encoder(self, encoder_input: Annotated[
        Optional[EncoderInput], Field(description="Encoder object to be added to the store")], db) -> JSONResponse:
        """Create a new encoder (Super User access required)."""
        result = await db.execute(select(encoder_table).where(or_(encoder_table.id == encoder_input.id)))
        existing = result.scalars().first()
        if existing:
            raise HTTPException(status_code=400, detail="encoder already exists")

        # Create and save experiment
        data = encoder_input.model_dump(exclude_none=True, by_alias=False)
        data["id"] = json.dumps(data["id"])
        data["name"] = json.dumps(data["name"])
        data["encoder_type"] = json.dumps(data["encoder_type"])
        data["comment"] = json.dumps(data["comment"])
        data["scalable"] = json.dumps(data["scalable"])
        data["noOfLayers"] = json.dumps(data["noOfLayers"])
        data["path"] = json.dumps(data["path"])
        # data["filename"] = json.dumps(data["filename"])
        data["modeFileReq"] = json.dumps(data["modeFileReq"])
        # data["SeqFileReq"] = json.dumps(data["seqFileReq"])
        data["layersFileReq"] = json.dumps(data["layersFileReq"])

        data = clean_input(data)

        db_obj = encoder_table(**data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return JSONResponse(status_code=200, content={"message": "Encoder created successfully"})

    async def delete_encoder(self, id: StrictInt, db) -> JSONResponse:
        """Delete a specific encoder (Super User access required)."""
        db_obj = await db.execute(select(encoder_table).filter(encoder_table.id == id))
        encoder_info = db_obj.scalars().first()

        if not encoder_info:
            raise HTTPException(status_code=404, detail="Encoder not found")

        await db.delete(encoder_info)
        await db.commit()
        return JSONResponse(status_code=200, content={"message": "Encoder deleted"})

    async def get_encoder(self, id: StrictInt, db) -> Encoder:
        """Fetch a specific encoder by ID."""
        db_obj = await db.execute(select(encoder_table).filter(encoder_table.id == id))
        encoder = db_obj.scalars().first()

        if not encoder:
            raise HTTPException(status_code=404, detail="Encoder not found")

        return encoder

    async def get_encoders(self, db) -> List[Encoder]:
        """Fetch a list of all encoders."""
        db_obj = await db.execute(select(encoder_table))
        all_encoders = db_obj.scalars()

        if not all_encoders:
            return []

        return all_encoders

    async def update_encoder(self, id: StrictInt, db, encoder_input: Annotated[
        Optional[EncoderInput], Field(description="Encoder object to be added to the store")], ) -> JSONResponse:
        """Update an existing encoder (Super User access required)."""
        """This can only be done by the user who owns the experiment."""
        result = await db.execute(select(encoder_table).where(encoder_table.id == id))
        encoder = result.scalars().first()

        if not encoder:
            raise HTTPException(status_code=404, detail="Encoder not found")

        # Step 2: Prepare data
        data = encoder_input.model_dump(exclude_none=True, by_alias=False)

        # Optional: Clean the input data if needed
        data = clean_input(data)  # use your existing clean_input() method

        # Step 3: Update fields
        for key, value in data.items():
            setattr(encoder, key, value)

        # Step 4: Commit changes
        await db.commit()
        await db.refresh(encoder)

        return JSONResponse(status_code=200, content={"message": f"Encoder {id} updated successfully"})


def clean_input(data: dict) -> dict:
    bool_fields = ["scalable", "modeFileReq", "seqFileReq", "layersFileReq"]
    int_fields = ["id", "noOfLayers"]

    cleaned = {}
    for key, val in data.items():
        if key in bool_fields:
            if isinstance(val, str):
                cleaned[key] = val.lower() == "true"
            else:
                cleaned[key] = bool(val)
        elif key in int_fields:
            if isinstance(val, str):
                cleaned[key] = int(val)
            else:
                cleaned[key] = val
        else:
            # Remove extra quotes if present
            if isinstance(val, str) and val.startswith('"') and val.endswith('"'):
                cleaned[key] = val[1:-1]
            else:
                cleaned[key] = val
    return cleaned
