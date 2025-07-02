import io
import os
import zipfile
from datetime import datetime
from pathlib import Path

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import select, func
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from app.database.tables.experiments import Experiment as ExperimentTable, Experiment
from app.database.tables.results import ExperimentResult
from app.models.experiment import ExperimentStatus
from app.models.user import User
from app.routers.results import user_dependency


@pytest.fixture(autouse=True)
def override_user_dep(app):
    mock_user = User(
        id=1,
        username="testuser",
        password="fake",
        role="user",
        email="test@example.com",
        first_name="Test",
        last_name="User"
    )
    app.dependency_overrides[user_dependency] = lambda: mock_user


@pytest_asyncio.fixture
async def create_experiment(db):
    async def _create():
        exp = ExperimentTable(
            experiment_name="UploadTest",
            description="Test upload results",
            owner_id=1,
            status=ExperimentStatus.COMPLETE,
            created_at=datetime.now().isoformat()
        )
        db.add(exp)
        await db.commit()
        await db.refresh(exp)
        return exp
    return _create


@pytest.mark.asyncio
class TestResultsRoutes:

    async def test_upload_results_file_success(self, async_client: AsyncClient, db, isolate_upload_dir, create_experiment):
        experiment = await create_experiment()

        file_content = b"Some result data"
        response = await async_client.post(
            f"/experiments/{experiment.id}/results",
            files={"file": ("result1.txt", io.BytesIO(file_content), "text/plain")}
        )

        assert response.status_code == HTTP_200_OK
        assert response.json()["message"] == "File uploaded successfully"

        result_count = (await db.execute(select(func.count()).select_from(ExperimentResult))).scalar_one()
        assert result_count == 1

        db_result = (
            await db.execute(select(ExperimentResult).where(ExperimentResult.experiment_id == experiment.id))
        ).scalars().first()

        assert db_result.filename == "result1.txt"

        expected_path = Path(isolate_upload_dir) / "results" / str(experiment.id) / "result1.txt"
        assert expected_path.exists()

    async def test_get_experiment_results(self, async_client: AsyncClient, db, isolate_upload_dir):
        exp = Experiment(
            id=9001,
            experiment_name="GetTest",
            description="Test get results",
            owner_id=1,
            status=ExperimentStatus.COMPLETE,
            created_at=datetime.now().isoformat()
        )
        db.add(exp)
        await db.commit()

        uploaded_filenames = []
        for i in range(2):
            filename = f"file{i}.txt"
            content = f"content of file {i}".encode()
            uploaded_filenames.append(filename)

            result_path = os.path.join(isolate_upload_dir, "results", str(exp.id))
            os.makedirs(result_path, exist_ok=True)
            full_file_path = os.path.join(result_path, filename)
            with open(full_file_path, "wb") as f:
                f.write(content)

            db_result = ExperimentResult(
                filename=filename,
                path=full_file_path,
                experiment_id=exp.id
            )
            db.add(db_result)

        await db.commit()

        zip_response = await async_client.get(f"/experiments/{exp.id}/results")
        assert zip_response.status_code == HTTP_200_OK
        assert zip_response.headers["content-type"] == "application/zip"

        with zipfile.ZipFile(io.BytesIO(zip_response.content)) as z:
            names_in_zip = z.namelist()
            assert set(names_in_zip) == set(uploaded_filenames)

            for name in names_in_zip:
                with z.open(name) as f:
                    content = f.read().decode()
                    assert "content of file" in content

    async def test_upload_duplicate_filename(self, async_client: AsyncClient, db, create_experiment):
        experiment = await create_experiment()
        filename = "duplicate.txt"
        content = b"test data"

        res1 = await async_client.post(
            f"/experiments/{experiment.id}/results",
            files={"file": (filename, io.BytesIO(content), "text/plain")}
        )
        assert res1.status_code == HTTP_200_OK

        res2 = await async_client.post(
            f"/experiments/{experiment.id}/results",
            files={"file": (filename, io.BytesIO(content), "text/plain")}
        )
        assert res2.status_code == HTTP_400_BAD_REQUEST
        assert "already been uploaded" in res2.json()["detail"]

    async def test_get_results_not_found(self, async_client: AsyncClient, db):
        exp = ExperimentTable(
            experiment_name="NoResults",
            description="No files here",
            owner_id=1,
            status=ExperimentStatus.COMPLETE,
            created_at=datetime.now().isoformat()
        )
        db.add(exp)
        await db.commit()
        await db.refresh(exp)

        response = await async_client.get(f"/experiments/{exp.id}/results")
        assert response.status_code == HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "No result files found for experiment"
