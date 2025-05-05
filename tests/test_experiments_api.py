from fastapi.testclient import TestClient


from pydantic import Field, StrictBytes, StrictStr  # noqa: F401
from typing import Any, List, Optional, Tuple, Union  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from app.models.error import Error  # noqa: F401
from app.models.experiment import Experiment  # noqa: F401
from app.models.experiment_input import ExperimentInput  # noqa: F401
from app.models.experiment_status import ExperimentStatus  # noqa: F401


def test_create_experiment(client: TestClient):
    """Test case for create_experiment

    Create a new experiment.
    """
    experiment_input = {"network_conditions":{"delay":"100ms","packet_loss":"1%"},"metrics_requested":["PSNR","SSIM"],"encoding_parameters":{"codec":"H.264","bitrate":"5000kbps","resolution":"1920x1080"},"description":"Experiment description text here","video_sources":["video1.mp4","video2.mp4"],"experiment_name":"Video Encoding Test"}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/experiments",
    #    headers=headers,
    #    json=experiment_input,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_delete_experiment(client: TestClient):
    """Test case for delete_experiment

    Delete an experiment.
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/experiments/{experimentId}".format(experimentId='experiment_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_experiment(client: TestClient):
    """Test case for get_experiment

    Get experiment by ID.
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/experiments/{experimentId}".format(experimentId='experiment_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_experiment_results(client: TestClient):
    """Test case for get_experiment_results

    Get results for an experiment.
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/experiments/{experimentId}/results".format(experimentId='experiment_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_experiment_status(client: TestClient):
    """Test case for get_experiment_status

    Get experiment status
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/experiments/{experimentId}/status".format(experimentId='experiment_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_experiments(client: TestClient):
    """Test case for get_experiments

    List experiments.
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/experiments",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_update_experiment(client: TestClient):
    """Test case for update_experiment

    Update an experiment.
    """
    experiment_input = {"network_conditions":{"delay":"100ms","packet_loss":"1%"},"metrics_requested":["PSNR","SSIM"],"encoding_parameters":{"codec":"H.264","bitrate":"5000kbps","resolution":"1920x1080"},"description":"Experiment description text here","video_sources":["video1.mp4","video2.mp4"],"experiment_name":"Video Encoding Test"}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/experiments/{experimentId}".format(experimentId='experiment_id_example'),
    #    headers=headers,
    #    json=experiment_input,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_upload_results(client: TestClient):
    """Test case for upload_results

    Upload results for an experiment.
    """

    headers = {
    }
    data = {
        "filename": ['/path/to/file']
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/experiments/{experimentId}/results".format(experimentId='experiment_id_example'),
    #    headers=headers,
    #    data=data,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

