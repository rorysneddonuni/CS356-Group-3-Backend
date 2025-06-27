import os.path
import zipfile
from io import BytesIO
from typing import ClassVar
from typing import Tuple

from fastapi import UploadFile, HTTPException
from pydantic import Field, StrictStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from starlette.responses import StreamingResponse
from typing_extensions import Annotated

from app.config.settings import Settings
from app.database.tables.experiments import Experiment
from app.database.tables.results import ExperimentResult
from app.models.info import Info
from app.models.user import User
from app.services.utility.files import upload_file


class ResultsService:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        ResultsService.subclasses = ResultsService.subclasses + (cls,)

    async def get_experiment_results(self, experiment_id: Annotated[
        StrictStr, Field(description="ID to uniquely identify an experiment.")], current_user: User,
                                     db: AsyncSession) -> StreamingResponse:
        """Get list of files to download for results."""
        experiment = await self.get_experiment(experiment_id, db, current_user)

        if not experiment.result_files:
            raise HTTPException(status_code=404, detail="No result files found for experiment")

        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for result in experiment.result_files:
                if not os.path.exists(result.path):
                    continue
                zf.write(result.path, arcname=result.filename)
        zip_buffer.seek(0)
        return StreamingResponse(zip_buffer, media_type='application/zip', headers={
            "Content-Disposition": f"attachment; filename={experiment.experiment_name}_results.zip"})

    async def upload_result(self, experiment_id: int, file: UploadFile, db: AsyncSession, settings: Settings,
                            current_user: User) -> Info:
        experiment = await self.get_experiment(experiment_id, db, current_user)

        results = await db.execute(select(ExperimentResult).where(ExperimentResult.experiment_id == experiment_id,
                                                                  ExperimentResult.filename == file.filename))

        if results.scalars().first():
            raise HTTPException(status_code=400,
                                detail="File with this name has already been uploaded for this experiment")

        path = upload_file(file, settings.uploads_directory, "results", str(experiment_id))

        result = ExperimentResult(filename=file.filename, experiment_id=experiment.id, path=str(path))
        db.add(result)
        await db.commit()

        return Info(message="File uploaded successfully")

    async def get_experiment(self, experiment_id: int, db: AsyncSession, current_user: User) -> Experiment:
        experiments = await db.execute(
            select(Experiment).options(joinedload(Experiment.result_files)).where(Experiment.id == experiment_id))
        experiment = experiments.scalars().first()

        if not experiment:
            raise HTTPException(status_code=404, detail="Experiment not found")

        if current_user.id != experiment.owner_id and current_user.role not in ('admin', 'super_user'):
            raise HTTPException(status_code=403, detail="You are not authorized to access this resource")

        return experiment


class ResultsServiceImpl(ResultsService):
    ...
