from fastapi.testclient import TestClient


from pydantic import StrictBytes, StrictStr  # noqa: F401
from typing import List, Optional, Tuple, Union  # noqa: F401
from app.models.error import Error  # noqa: F401
from app.models.video import Video  # noqa: F401


def test_create_video(client: TestClient):
    """Test case for create_video

    Create video
    """

    headers = {
    }
    data = {
        "video": '/path/to/file',
        "frame_rate": 'frame_rate_example',
        "resolution": 'resolution_example'
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/infrastructure/videos",
    #    headers=headers,
    #    data=data,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_delete_video(client: TestClient):
    """Test case for delete_video

    Delete video
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/infrastructure/videos/{id}".format(id='id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_video(client: TestClient):
    """Test case for get_video

    Retrieve video
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/infrastructure/videos/{id}".format(id='id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_videos(client: TestClient):
    """Test case for get_videos

    Retrieve videos list
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/infrastructure/videos",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

