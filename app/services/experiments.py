from typing import List, Optional, Union, ClassVar, Tuple

from pydantic import Field, StrictBytes, StrictStr
from typing_extensions import Annotated

from app.database.database import get_db
from app.models.experiment import Experiment
from app.models.experiment_input import ExperimentInput
from app.models.experiment_status import ExperimentStatus
from app.database.tables.experiments import ExperimentsTable

from fastapi import HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import utility.video_file_handler as video_file_handler


class ExperimentsService:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        ExperimentsService.subclasses = ExperimentsService.subclasses + (cls,)

    async def create_experiment(self, experiment_input: Annotated[Optional[ExperimentInput], Field(
        description="Experiment object that needs to be added to the store")], db: AsyncSession = Depends(get_db)) -> Experiment:
        # Check if experiment name already exists
        result = await db.execute(select(ExperimentsTable).where(
            or_(ExperimentsTable.experiment_name == experiment_input.experiment_name)))
        existing = result.scalars().first()
        if existing:
            raise HTTPException(status_code=400, detail="Experiment name already exists")

        # Create and save experiment
        db_obj = ExperimentsTable(**experiment_input.model_dump(exclude_none=True))
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        return Experiment.model_validate(db_obj.__dict__)

    async def delete_experiment(self, experiment_id: Annotated[
        StrictStr, Field(description="ID to uniquely identify an experiment.")], db: AsyncSession = Depends(get_db)) -> None:
        result = await db.execute(select(ExperimentsTable).where(ExperimentsTable.id == experiment_id))
        db_obj = result.scalars().first()
        if not db_obj:
            raise HTTPException(status_code=404, detail="Experiment not found")

        await db.delete(db_obj)
        await db.commit()
        return JSONResponse(status_code=200, content={"message": "User deleted"})

    async def get_experiment(self, experiment_id: Annotated[
        StrictStr, Field(description="ID to uniquely identify an experiment.")], db: AsyncSession = Depends(get_db)) -> Experiment:
        result = await db.execute(select(ExperimentsTable).where(ExperimentsTable.id == experiment_id))
        db_obj = result.scalars().first()
        if not db_obj:
            raise HTTPException(status_code=404, detail="Experiment not found")
        return Experiment.model_validate(db_obj.__dict__)

    async def get_experiment_status(self, experiment_id: Annotated[
        StrictStr, Field(description="Unique ID to identify the experiment.")], db: AsyncSession = Depends(get_db)) -> ExperimentStatus:
        result = await db.execute(select(ExperimentsTable).where(ExperimentsTable.id == experiment_id))
        db_obj = result.scalars().first()
        if not db_obj:
            raise HTTPException(status_code=404, detail="Experiment not found")
        return Experiment.status.model_validate(db_obj.__dict__)

    async def get_experiments(self, user_id: Annotated[
        StrictStr, Field(description="ID to uniquely identify a user.")], db: AsyncSession = Depends(get_db)) -> Experiment:
        result = await db.execute(select(ExperimentsTable).where(ExperimentsTable.owner_id == user_id))
        db_obj = result.scalars().first()
        if not db_obj:
            raise HTTPException(status_code=404, detail="No experiments found for user")
        return Experiment.model_validate(db_obj.__dict__)

    async def update_experiment(self, user_id: Annotated[
        StrictStr, Field(description="ID to uniquely identify the current user.")], experiment_id: Annotated[
        StrictStr, Field(description="ID to uniquely identify an experiment.")], experiment_input: Annotated[
        Optional[ExperimentInput], Field(
            description="Experiment object that needs to be added to the store")], db: AsyncSession = Depends(get_db)) -> None:
        """This can only be done by the user who owns the experiment."""
        result = await db.execute(select(ExperimentsTable).where(ExperimentsTable.id == experiment_id))
        db_obj = result.scalars().first()
        if not db_obj:
            raise HTTPException(status_code=404, detail="Experiment not found")
        experiment = result.scalars().first()
        if not experiment.owner_id == user_id:
            raise HTTPException(status_code=404, detail="Only the owner of the experiment can update the experiment")

        updates = experiment_input.model_dump(exclude_none=True)
        for field, value in updates.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        await db.commit()
        return Experiment.model_validate(db_obj.__dict__)

    async def upload_results(self, experiment_id: Annotated[
        StrictStr, Field(description="ID to uniquely identify an experiment.")],
        user_id: Annotated[StrictStr, Field(description="ID to uniquely identify an experiment.")],
        filename: Optional[List[Union[StrictBytes, StrictStr, Tuple[StrictStr, StrictBytes]]]], db: AsyncSession = Depends(get_db)) -> None:
        result = await db.execute(select(ExperimentsTable).where(ExperimentsTable.id == experiment_id))
        db_obj = result.scalars().first()
        if not user_id == db_obj.owner_id:
            raise HTTPException(status_code=501, detail="Only the owner of the experiment can access the results")
        if not db_obj:
            raise HTTPException(status_code=404, detail="No experiments found for user")
        # TODO: create and format file, work out what format is should be
        video_file_handler.store_video_file(...,filename)

    async def get_experiment_results(self, experiment_id: Annotated[
        StrictStr, Field(description="ID to uniquely identify an experiment.")],
                                     user_id: Annotated[
                                         StrictStr, Field(description="ID to uniquely identify a user.")],
                                     db: AsyncSession = Depends(get_db)) -> None:
        result = await db.execute(select(ExperimentsTable).where(ExperimentsTable.id == experiment_id))
        db_obj = result.scalars().first()
        if not user_id == db_obj.owner_id:
            raise HTTPException(status_code=501, detail="Only the owner of the experiment can access the results")
        if not db_obj:
            raise HTTPException(status_code=404, detail="No experiments found for user")
        return video_file_handler.retrieve_video_file(db_obj.results_location)
