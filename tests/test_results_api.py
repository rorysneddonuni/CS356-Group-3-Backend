import io
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


def test_get_experiment_results(client: TestClient):
    """Test case for get_experiment_results

    Get results for an experiment.
    """

    response = client.request("GET", "/experiments/{experimentId}/results".format(experimentId='9000'))

    assert response.status_code == 200


def test_upload_results(client: TestClient):
    """Test case for upload_results

    Upload results for an experiment.
    """

    headers = {}
    data = {"filename": ['/path/to/file']}
    response = client.request("POST",
        "/experiments/{experimentId}/results".format(experimentId='experiment_id_example'), headers=headers,
        data=data, )

    assert response.status_code == 200
