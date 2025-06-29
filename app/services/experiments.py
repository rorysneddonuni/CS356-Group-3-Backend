from datetime import datetime
from typing import Optional, ClassVar, Tuple, List

from fastapi import HTTPException
from pydantic import Field, StrictStr
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload
from starlette.responses import JSONResponse
from typing_extensions import Annotated

from sqlalchemy.exc import IntegrityError
from app.database.tables.experiments import Experiment as ExperimentTable, ExperimentSequence
from app.models.experiment import Experiment, ExperimentStatus, ExperimentInput, ExperimentUpdateInput
from app.models.experiment_sequence import ExperimentSequenceInput
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
        StrictStr, Field(description="ID to uniquely identify an experiment.")], user_id: str, db: AsyncSession) -> JSONResponse:
        db_experiment = await self._get_experiment_for_update(experiment_id, user_id, db)

        await db.delete(db_experiment)
        await db.commit()
        return JSONResponse(status_code=200, content={"message": "Experiment deleted"})

    async def get_experiment(self, experiment_id: Annotated[
        StrictStr, Field(description="ID to uniquely identify an experiment.")], db: AsyncSession,
                             user_id: Optional[int] = None) -> Experiment:
        result = await db.execute(select(ExperimentTable).options(
            selectinload(ExperimentTable.sequences).selectinload(ExperimentSequence.network_topology),
            selectinload(ExperimentTable.sequences).selectinload(ExperimentSequence.network_disruption_profile)).where(
            ExperimentTable.id == experiment_id))
        db_obj = result.scalars().first()
        if not db_obj:
            raise HTTPException(status_code=404, detail="Experiment not found")

        if user_id and db_obj.owner_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to access this experiment")

        return Experiment.model_validate(db_obj, from_attributes=True)

    async def get_experiments(self, user_id: Annotated[StrictStr, Field(description="ID to uniquely identify a user.")],
                              db: AsyncSession) -> List[Experiment]:
        result = await db.execute(select(ExperimentTable).options(
            selectinload(ExperimentTable.sequences).selectinload(ExperimentSequence.network_topology),
            selectinload(ExperimentTable.sequences).selectinload(ExperimentSequence.network_disruption_profile)).where(
            ExperimentTable.owner_id == user_id))
        db_objs = result.unique().scalars().all()

        if not db_objs:
            return []

        return [Experiment.model_validate(obj) for obj in db_objs]

    async def get_all_experiments(self, db: AsyncSession) -> list[Experiment]:
        result = await db.execute(select(ExperimentTable).options(
            selectinload(ExperimentTable.sequences).selectinload(ExperimentSequence.network_topology),
            selectinload(ExperimentTable.sequences).selectinload(ExperimentSequence.network_disruption_profile)))
        experiments = result.unique().scalars().all()
        return [Experiment.model_validate(exp) for exp in experiments]

    async def update_experiment(self, user_id: int, experiment_id: str, experiment_input: ExperimentUpdateInput,
                                db: AsyncSession) -> Experiment:
        experiment = await self._get_experiment_for_update(experiment_id, user_id, db)

        await self._check_name_uniqueness(experiment_input.experiment_name, experiment, db)

        self._update_fields(experiment, experiment_input)

        await self._handle_add_sequences(experiment_input.add_sequences, experiment.id, db)
        await self._handle_remove_sequences(experiment_input.remove_sequence_ids, experiment.id, db)

        try:
            await db.commit()
        except IntegrityError:
            await db.rollback()
            raise HTTPException(status_code=400, detail="Experiment name must be unique")

        await db.refresh(experiment)
        return await self.get_experiment(experiment.id, db)

    async def _get_experiment_for_update(self, experiment_id: str, user_id: int, db: AsyncSession) -> ExperimentTable:
        result = await db.execute(
            select(ExperimentTable)
            .options(selectinload(ExperimentTable.sequences))
            .where(ExperimentTable.id == experiment_id)
        )
        experiment = result.scalar_one_or_none()
        if not experiment:
            raise HTTPException(status_code=404, detail="Experiment not found")

        if experiment.owner_id != user_id:
            role = await UsersService().get_user_role_by_id(user_id=user_id, db=db)
            if role not in ("admin", "super_admin"):
                raise HTTPException(status_code=400, detail="Only the owner can update the experiment")

        return experiment

    async def _check_name_uniqueness(self, new_name: Optional[str], experiment: ExperimentTable, db: AsyncSession):
        if new_name and new_name != experiment.experiment_name:
            result = await db.execute(
                select(ExperimentTable).where(ExperimentTable.experiment_name == new_name)
            )
            existing = result.scalar_one_or_none()
            if existing and existing.id != experiment.id:
                raise HTTPException(status_code=400, detail="Experiment name already exists")

    def _update_fields(self, experiment: ExperimentTable, input_data: ExperimentUpdateInput):
        if input_data.experiment_name:
            experiment.experiment_name = input_data.experiment_name
        if input_data.description:
            experiment.description = input_data.description
        if input_data.status:
            experiment.status = input_data.status

    async def _handle_add_sequences(self, sequences_data: List[ExperimentSequenceInput], experiment_id: int,
                                    db: AsyncSession):
        for seq_input in sequences_data:
            new_seq = ExperimentSequence(
                **seq_input.model_dump(exclude_unset=True, by_alias=False),
                parent_experiment_id=experiment_id
            )
            db.add(new_seq)

    async def _handle_remove_sequences(self, sequence_ids: List[int], experiment_id: int, db: AsyncSession):
        if sequence_ids:
            await db.execute(
                delete(ExperimentSequence).where(
                    ExperimentSequence.sequence_id.in_(sequence_ids),
                    ExperimentSequence.parent_experiment_id == experiment_id
                )
            )

