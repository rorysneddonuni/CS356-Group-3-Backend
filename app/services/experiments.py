from datetime import datetime
from typing import Optional, ClassVar, Tuple, List

from fastapi import HTTPException
from pydantic import Field, StrictStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload
from starlette.responses import JSONResponse
from typing_extensions import Annotated

from sqlalchemy.exc import IntegrityError
from app.database.tables.experiments import Experiment as ExperimentTable, ExperimentSequence
from app.models.experiment import Experiment, ExperimentStatus, ExperimentInput
from app.services.users import UsersService


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
        experiment = ExperimentTable(
            **{**experiment_input.model_dump(), "owner_id": user_id, "status": ExperimentStatus.PENDING,
               "created_at": datetime.now(), "sequences": []})
        db.add(experiment)
        await db.commit()
        await db.refresh(experiment)

        # Create nested sequences
        for sequence in experiment_input.sequences:
            db_sequence = ExperimentSequence(**{**sequence.model_dump(), "parent_experiment_id": experiment.id})
            db.add(db_sequence)
        await db.commit()

        return Experiment.model_validate(await self.get_experiment(experiment.id, db))

    async def delete_experiment(self, experiment_id: Annotated[
        StrictStr, Field(description="ID to uniquely identify an experiment.")], db: AsyncSession) -> JSONResponse:
        db_experiment = await self.get_experiment(experiment_id, db)

        await db.delete(db_experiment)
        await db.commit()
        return JSONResponse(status_code=200, content={"message": "Experiment deleted"})

    async def get_experiment(self, experiment_id: Annotated[
        StrictStr, Field(description="ID to uniquely identify an experiment.")], db: AsyncSession) -> Experiment:
        result = await db.execute(select(ExperimentTable).options(
            selectinload(ExperimentTable.sequences).selectinload(ExperimentSequence.network_topology),
            selectinload(ExperimentTable.sequences).selectinload(ExperimentSequence.network_disruption_profile)).where(
            ExperimentTable.id == experiment_id))
        db_obj = result.scalars().first()
        if not db_obj:
            raise HTTPException(status_code=404, detail="Experiment not found")
        return Experiment.model_validate(db_obj, from_attributes=True)

    async def get_experiments(self, user_id: Annotated[StrictStr, Field(description="ID to uniquely identify a user.")],
                              db: AsyncSession) -> List[Experiment]:
        result = await db.execute(select(ExperimentTable).options(
            selectinload(ExperimentTable.sequences).selectinload(ExperimentSequence.network_topology),
            selectinload(ExperimentTable.sequences).selectinload(ExperimentSequence.network_disruption_profile)).where(
            ExperimentTable.owner_id == user_id))
        db_objs = result.unique().scalars().all()

        if not db_objs:
            raise HTTPException(status_code=404, detail="No experiments found for user")

        return [Experiment.model_validate(obj) for obj in db_objs]

    async def get_all_experiments(self, db: AsyncSession) -> list[Experiment]:
        result = await db.execute(select(ExperimentTable).options(
            selectinload(ExperimentTable.sequences).selectinload(ExperimentSequence.network_topology),
            selectinload(ExperimentTable.sequences).selectinload(ExperimentSequence.network_disruption_profile)))
        experiments = result.unique().scalars().all()
        if not experiments:
            raise HTTPException(status_code=404, detail="No experiments found")
        return [Experiment.model_validate(exp) for exp in experiments]

    async def update_experiment(self, user_id: int, experiment_id: str, experiment_input: ExperimentInput,
                                db: AsyncSession):
        result = await db.execute(
            select(ExperimentTable).where(ExperimentTable.id == experiment_id)
        )
        experiment = result.scalar_one_or_none()

        if not experiment:
            raise HTTPException(status_code=404, detail="Experiment not found")

        if experiment.owner_id != user_id:
            role = await UsersService().get_user_role_by_id(user_id=user_id, db=db)
            if role not in ("admin", "super_admin"):
                raise HTTPException(status_code=400, detail="Only the owner can update the experiment")

        update_data = experiment_input.model_dump(exclude_unset=True, by_alias=False)

        for field, value in update_data.items():
            if field in experiment.__table__.columns:
                setattr(experiment, field, value)

        try:
            await db.commit()
        except IntegrityError:
            await db.rollback()
            raise HTTPException(status_code=400, detail="Experiment name must be unique")

        await db.refresh(experiment)
        return await self.get_experiment(experiment.id, db)
