from fastapi.testclient import TestClient


from pydantic import Field, StrictBytes, StrictStr  # noqa: F401
from typing import Any, List, Optional, Tuple, Union  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from app.models.error import Error  # noqa: F401


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

