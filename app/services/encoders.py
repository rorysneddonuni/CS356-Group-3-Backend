# app/services/encoders.py

import logging
from typing import List, ClassVar, Tuple

from fastapi import HTTPException
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.inspection import inspect

from app.database.tables.encoder import Encoder as encoder_table
from app.models.encoder import Encoder as EncoderModel
from app.models.encoder_input import EncoderInput

logger = logging.getLogger(__name__)

class EncodersService:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        EncodersService.subclasses += (cls,)

    def safe_dict(self, obj):
        return {
            c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs
        }

    async def create_encoder(self, inp: EncoderInput, db: AsyncSession) -> EncoderModel:
        logger.info(f"Creating encoder: {inp.name!r}")
        # uniqueness check
        existing = await db.execute(
            select(encoder_table).where(encoder_table.name == inp.name)
        )
        if existing.scalars().first():
            raise HTTPException(status_code=400, detail="Encoder name already exists")

        data = inp.model_dump(exclude_none=True)  # field names match table attrs
        data.pop("id", None)
        db_obj = encoder_table(**data)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return EncoderModel.model_validate(self.safe_dict(db_obj))

    async def get_encoders(self, db: AsyncSession) -> List[EncoderModel]:
        logger.info("Retrieving all encoders")
        result = await db.execute(select(encoder_table))
        return [
            EncoderModel.model_validate(self.safe_dict(o))
            for o in result.scalars().all()
        ]

    async def get_encoder(self, id: int, db: AsyncSession) -> EncoderModel:
        logger.info(f"Retrieving encoder id={id}")
        result = await db.execute(
            select(encoder_table).where(encoder_table.id == id)
        )
        obj = result.scalars().first()
        if not obj:
            raise HTTPException(status_code=404, detail="Encoder not found")
        return EncoderModel.model_validate(self.safe_dict(obj))

    async def update_encoder(self, id: int, inp: EncoderInput, db: AsyncSession) -> EncoderModel:
        logger.info(f"Updating encoder id={id}")
        result = await db.execute(
            select(encoder_table).where(encoder_table.id == id)
        )
        obj = result.scalars().first()
        if not obj:
            raise HTTPException(status_code=404, detail="Encoder not found")

        data = inp.model_dump(exclude_none=True)
        data.pop("id", None)

        # if name changed, check uniqueness
        if "name" in data and data["name"] != obj.name:
            dup = await db.execute(
                select(encoder_table).where(encoder_table.name == data["name"])
            )
            if dup.scalars().first():
                raise HTTPException(status_code=400, detail="Encoder name already exists")

        for k, v in data.items():
            setattr(obj, k, v)

        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return EncoderModel.model_validate(self.safe_dict(obj))

    async def delete_encoder(self, id: int, db: AsyncSession) -> Response:
        logger.info(f"Deleting encoder id={id}")
        result = await db.execute(
            select(encoder_table).where(encoder_table.id == id)
        )
        obj = result.scalars().first()
        if not obj:
            raise HTTPException(status_code=404, detail="Encoder not found")
        await db.delete(obj)
        await db.commit()
        return Response(status_code=204)

class SqliteEncodersService(EncodersService):
    pass
