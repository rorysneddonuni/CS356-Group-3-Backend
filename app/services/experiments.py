from datetime import datetime
from typing import Optional, ClassVar, Tuple, List

from fastapi import HTTPException
from pydantic import Field, StrictStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from starlette.responses import JSONResponse
from typing_extensions import Annotated

from app.database.tables.experiments import Experiment as ExperimentTable
from app.models.experiment import Experiment, ExperimentStatus, ExperimentInput


class ExperimentsService:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        ExperimentsService.subclasses = ExperimentsService.subclasses + (cls,)

    async def create_experiment(self, user_id: str, experiment_input: Annotated[
        Optional[ExperimentInput], Field(description="Experiment object that needs to be added to the store")],
                                db: AsyncSession) -> Experiment:
        # Check if experiment name already exists
        result = await db.execute(select(ExperimentTable).options(joinedload(ExperimentTable.sequences)).where(
            ExperimentTable.experiment_name == experiment_input.experiment_name))
        existing = result.scalars().first()
        if existing:
            raise HTTPException(status_code=400, detail="Experiment name already exists")
        # Create and save experiment
        db_obj = ExperimentTable(
            **{**experiment_input.model_dump(), "owner_id": user_id, "status": ExperimentStatus.PENDING,
               "created_at": datetime.now()})
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        return Experiment.model_validate(await self.get_experiment(db_obj.id, db))

    async def delete_experiment(self, experiment_id: Annotated[
        StrictStr, Field(description="ID to uniquely identify an experiment.")], db: AsyncSession) -> JSONResponse:
        db_experiment = await self.get_experiment(experiment_id, db)

        await db.delete(db_experiment)
        await db.commit()
        return JSONResponse(status_code=200, content={"message": "Experiment deleted"})

    async def get_experiment(self, experiment_id: Annotated[
        StrictStr, Field(description="ID to uniquely identify an experiment.")], db: AsyncSession) -> Experiment:
        result = await db.execute(select(ExperimentTable).options(joinedload(ExperimentTable.sequences)).where(
            ExperimentTable.id == experiment_id))
        db_obj = result.scalars().first()
        if not db_obj:
            raise HTTPException(status_code=404, detail="Experiment not found")
        return Experiment.model_validate(db_obj, from_attributes=True)

    async def get_experiments(self, user_id: Annotated[StrictStr, Field(description="ID to uniquely identify a user.")],
                              db: AsyncSession) -> List[Experiment]:
        result = await db.execute(select(ExperimentTable).options(joinedload(ExperimentTable.sequences)).where(
            ExperimentTable.owner_id == user_id))
        db_objs = result.unique().scalars().all()

        if not db_objs:
            raise HTTPException(status_code=404, detail="No experiments found for user")

        return [Experiment.model_validate(obj) for obj in db_objs]

    async def get_all_experiments(self, db: AsyncSession) -> list[Experiment]:
        result = await db.execute(select(ExperimentTable).options(joinedload(ExperimentTable.sequences)))
        experiments = result.unique().scalars().all()
        if not experiments:
            raise HTTPException(status_code=404, detail="No experiments found")
        return [Experiment.model_validate(exp) for exp in experiments]

    async def update_experiment(self, user_id: Annotated[
        StrictStr, Field(description="ID to uniquely identify the current user.")], experiment_id: Annotated[
        StrictStr, Field(description="ID to uniquely identify an experiment.")], experiment_input: Annotated[
        Optional[ExperimentInput], Field(description="Experiment object that needs to be added to the store")],
                                db: AsyncSession) -> Experiment:
        """This can only be done by the user who owns the experiment."""
        experiment = await self.get_experiment(experiment_id, db)

        if not experiment.owner_id == user_id:
            raise HTTPException(status_code=400, detail="Only the owner of the experiment can update the experiment")

        for field, value in experiment_input.model_dump().items():
            setattr(experiment, field, value)

        await db.commit()
        await db.refresh(experiment)
        return Experiment.model_validate(await self.get_experiment(experiment.id, db))
