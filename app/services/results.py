import os.path
import zipfile
from io import BytesIO
from typing import ClassVar
from typing import Tuple

from fastapi import UploadFile, HTTPException
from pydantic import Field, StrictStr
from starlette.responses import StreamingResponse, JSONResponse
from typing_extensions import Annotated

from app.database.database import SessionDep
from app.database.tables.experiments import ExperimentResult, Experiment
from app.models.info import Info
from app.services.utility.files import upload_file


class ResultsService:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        ResultsService.subclasses = ResultsService.subclasses + (cls,)

    async def get_experiment_results(self, experiment_id: Annotated[
        StrictStr, Field(description="ID to uniquely identify an experiment.")], db: SessionDep) -> StreamingResponse:
        """Get list of files to download for results."""
        # todo user authentication
        experiment = db.query(Experiment).filter(Experiment.id == experiment_id).first()
        if not experiment:
            raise HTTPException(status_code=404, detail="Experiment not found")

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

    async def upload_result(self, experiment_id: int, file: UploadFile, db: SessionDep) -> Info:
        if db.query(ExperimentResult).filter(ExperimentResult.experiment_id == experiment_id).filter(
                ExperimentResult.filename == file.filename).first():
            raise HTTPException(status_code=400,
                                detail="File with this name has already been uploaded for this experiment")

        path = upload_file(file, "results", str(experiment_id))

        result = ExperimentResult(filename=file.filename, experiment_id=experiment_id, path=str(path))
        db.add(result)
        db.commit()

        return Info(message="File uploaded successfully")


class ResultsServiceImpl(ResultsService):
    ...
