import io
import zipfile
from pathlib import Path
from typing import Any, List, Optional, Tuple, Union  # noqa: F401

from fastapi.testclient import TestClient
from pydantic import Field, StrictBytes, StrictStr  # noqa: F401
from typing_extensions import Annotated  # noqa: F401

from app.database.tables.experiments import Experiment, ExperimentResult
from app.models.error import Error  # noqa: F401


def test_upload_results_file_success(client, db, isolate_upload_dir):
    expected_id = 9000
    exp = Experiment(id=expected_id, name="UploadTest", description="Test upload results", owner_id="1", status="TEST",
                     codec="", bitrate="", resolution="")
    db.add(exp)
    db.commit()

    file_content = b"Some result data"
    response = client.post(f"/experiments/{exp.id}/results",
                           files={"file": ("result1.txt", io.BytesIO(file_content), "text/plain")})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "File uploaded successfully"
    assert db.query(ExperimentResult).count() == 1
    db_result = db.query(ExperimentResult).filter(ExperimentResult.experiment_id == exp.id).first()
    assert db_result.filename == "result1.txt"
    assert Path(isolate_upload_dir + '/results/9000/result1.txt').exists()


def test_get_experiment_results(client: TestClient, db, isolate_upload_dir):
    """Test case for get_experiment_results

    Get results for an experiment.
    """
    expected_id = 9000
    exp = Experiment(id=expected_id, name="UploadTest", description="Test upload results", owner_id="1", status="TEST",
                     codec="", bitrate="", resolution="")
    db.add(exp)
    db.commit()

    uploaded_filenames = []
    for i in range(2):
        filename = f"file{i}.txt"
        file_content = f"content of file {i}".encode()
        uploaded_filenames.append(filename)

        response = client.post(f"/experiments/{exp.id}/results",
                               files={"file": (filename, io.BytesIO(file_content), "text/plain")}, )
        assert response.status_code == 200

    zip_response = client.get(f"/experiments/{exp.id}/results")
    assert zip_response.status_code == 200
    assert zip_response.headers["content-type"] == "application/zip"

    with zipfile.ZipFile(io.BytesIO(zip_response.content)) as z:
        names_in_zip = z.namelist()
        assert set(names_in_zip) == set(uploaded_filenames)

        for name in names_in_zip:
            with z.open(name) as f:
                content = f.read().decode()
                assert f"content of file" in content


def test_upload_duplicate_filename(client, db):
    # Create an experiment
    exp = Experiment(name="DuplicateTest", description="Test upload results", owner_id="1", status="TEST", codec="",
                     bitrate="", resolution="")
    db.add(exp)
    db.commit()

    filename = "result.csv"
    content = b"test data"

    # First upload
    response1 = client.post(f"/experiments/{exp.id}/results",
        files={"file": (filename, io.BytesIO(content), "text/csv")}, )
    assert response1.status_code == 200

    # Second upload with same name
    response2 = client.post(f"/experiments/{exp.id}/results",
        files={"file": (filename, io.BytesIO(content), "text/csv")}, )
    assert response2.status_code == 400
    assert "File with this name has already been uploaded for this experiment" in response2.json()["detail"]
