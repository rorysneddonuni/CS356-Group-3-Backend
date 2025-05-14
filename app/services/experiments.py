from typing import Optional, ClassVar, Tuple

from fastapi import HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import Field, StrictStr
from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing_extensions import Annotated

from app.database.database import get_db
from app.database.tables.experiments import Experiment
from app.models.experiment import Experiment
from app.models.experiment_input import ExperimentInput
from app.models.experiment_status import ExperimentStatus


class ExperimentsService:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        ExperimentsService.subclasses = ExperimentsService.subclasses + (cls,)

    async def create_experiment(self, experiment_input: Annotated[
        Optional[ExperimentInput], Field(description="Experiment object that needs to be added to the store")],
                                db: AsyncSession = Depends(get_db)) -> Experiment:
        # Check if experiment name already exists
        result = await db.execute(
            select(Experiment).where(or_(Experiment.experiment_name == experiment_input.experiment_name)))
        existing = result.scalars().first()
        if existing:
            raise HTTPException(status_code=400, detail="Experiment name already exists")

        # Create and save experiment
        db_obj = Experiment(**experiment_input.model_dump(exclude_none=True))
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        return Experiment.model_validate(db_obj.__dict__)

    async def delete_experiment(self, experiment_id: Annotated[
        StrictStr, Field(description="ID to uniquely identify an experiment.")],
                                db: AsyncSession = Depends(get_db)) -> None:
        result = await db.execute(select(Experiment).where(Experiment.id == experiment_id))
        db_obj = result.scalars().first()
        if not db_obj:
            raise HTTPException(status_code=404, detail="Experiment not found")

        await db.delete(db_obj)
        await db.commit()
        return JSONResponse(status_code=200, content={"message": "User deleted"})

    async def get_experiment(self, experiment_id: Annotated[
        StrictStr, Field(description="ID to uniquely identify an experiment.")],
                             db: AsyncSession = Depends(get_db)) -> Experiment:
        result = await db.execute(select(Experiment).where(Experiment.id == experiment_id))
        db_obj = result.scalars().first()
        if not db_obj:
            raise HTTPException(status_code=404, detail="Experiment not found")
        return Experiment.model_validate(db_obj.__dict__)

    async def get_experiment_status(self, experiment_id: Annotated[
        StrictStr, Field(description="Unique ID to identify the experiment.")],
                                    db: AsyncSession = Depends(get_db)) -> ExperimentStatus:
        result = await db.execute(select(Experiment).where(Experiment.id == experiment_id))
        db_obj = result.scalars().first()
        if not db_obj:
            raise HTTPException(status_code=404, detail="Experiment not found")
        return Experiment.status.model_validate(db_obj.__dict__)

    async def get_experiments(self, user_id: Annotated[StrictStr, Field(description="ID to uniquely identify a user.")],
                              db: AsyncSession = Depends(get_db)) -> Experiment:
        result = await db.execute(select(Experiment).where(Experiment.owner_id == user_id))
        db_obj = result.scalars().first()
        if not db_obj:
            raise HTTPException(status_code=404, detail="No experiments found for user")
        return Experiment.model_validate(db_obj.__dict__)

    async def update_experiment(self, user_id: Annotated[
        StrictStr, Field(description="ID to uniquely identify the current user.")], experiment_id: Annotated[
        StrictStr, Field(description="ID to uniquely identify an experiment.")], experiment_input: Annotated[
        Optional[ExperimentInput], Field(description="Experiment object that needs to be added to the store")],
                                db: AsyncSession = Depends(get_db)) -> None:
        """This can only be done by the user who owns the experiment."""
        result = await db.execute(select(Experiment).where(Experiment.id == experiment_id))
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
