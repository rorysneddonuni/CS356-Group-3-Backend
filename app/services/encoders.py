import json
import uuid
from typing import ClassVar, Tuple
from typing import List, Optional

from fastapi import HTTPException
from pydantic import Field, StrictInt
from pydantic.v1 import StrictStr
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
        # Create and save experiment
        data = encoder_input.model_dump(exclude_none=True, by_alias=False)

        data["id"] = str(uuid.uuid4())
        data["video_id"] = json.dumps(data["video_id"])
        data["duration"] = json.dumps(data["duration"])
        data["frames_to_encode"] = json.dumps(data["frames_to_encode"])
        data["fps"] = json.dumps(data["fps"])
        data["res_width"] = json.dumps(data["res_width"])
        data["res_height"] = json.dumps(data["res_height"])
        data["input_file_title"] = json.dumps(data["input_file_title"])
        data["encoder"] = json.dumps(data["encoder"])
        data["encoder_type"] = json.dumps(data["encoder_type"])
        data["bit_rate"] = json.dumps(data["bit_rate"])
        data["yuv_format"] = json.dumps(data["yuv_format"])
        data["encoder_mode"] = json.dumps(data["encoder_mode"])
        data["quality"] = json.dumps(data["quality"])
        data["bit_depth"] = json.dumps(data["bit_depth"])
        data["infrared_period"] = json.dumps(data["infrared_period"])
        data["b_frames"] = json.dumps(data["b_frames"])
        data["max_no_layers"] = json.dumps(data["max_no_layers"])

        # data = clean_input(data)

        db_obj = encoder_table(**data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return JSONResponse(status_code=200, content={"message": "Encoder created successfully"})

    async def delete_encoder(self, id: StrictStr, db) -> JSONResponse:
        """Delete a specific encoder (Super User access required)."""
        db_obj = await db.execute(select(encoder_table).filter(encoder_table.id == id))
        encoder_info = db_obj.scalars().first()

        if not encoder_info:
            raise HTTPException(status_code=404, detail="Encoder not found")

        await db.delete(encoder_info)
        await db.commit()
        return JSONResponse(status_code=200, content={"message": "Encoder deleted"})

    async def get_encoder(self, id: StrictStr, db) -> Encoder:
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
            raise HTTPException(status_code=404, detail="No encoders found")

        return all_encoders

    async def update_encoder(self, id: StrictStr, db, encoder_input: Annotated[
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
