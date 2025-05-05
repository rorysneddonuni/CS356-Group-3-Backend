from fastapi.testclient import TestClient


from pydantic import Field, StrictInt  # noqa: F401
from typing import Any, List, Optional  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from app.models.encoder import Encoder  # noqa: F401
from app.models.encoder_input import EncoderInput  # noqa: F401
from app.models.error import Error  # noqa: F401


def test_create_encoder(client: TestClient):
    """Test case for create_encoder

    Create encoder
    """
    encoder_input = {"name":"name","encoder_code":"encoderCode","layers":["",""],"id":0,"encoder_type":"encoderType"}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/infrastructure/encoders",
    #    headers=headers,
    #    json=encoder_input,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_delete_encoder(client: TestClient):
    """Test case for delete_encoder

    Delete encoder
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/infrastructure/encoders/{id}".format(id=56),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_encoder(client: TestClient):
    """Test case for get_encoder

    Retrieve encoder
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/infrastructure/encoders/{id}".format(id=56),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_encoders(client: TestClient):
    """Test case for get_encoders

    Retrieve encoder list
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/infrastructure/encoders",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_update_encoder(client: TestClient):
    """Test case for update_encoder

    Update encoder
    """
    encoder_input = {"name":"name","encoder_code":"encoderCode","layers":["",""],"id":0,"encoder_type":"encoderType"}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/infrastructure/encoders/{id}".format(id=56),
    #    headers=headers,
    #    json=encoder_input,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

