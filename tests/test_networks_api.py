from fastapi.testclient import TestClient


from pydantic import Field, StrictStr  # noqa: F401
from typing import Any, List, Optional  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from app.models.error import Error  # noqa: F401
from app.models.network import Network  # noqa: F401
from app.models.network_input import NetworkInput  # noqa: F401


def test_create_network(client: TestClient):
    """Test case for create_network

    Create network
    """
    network_input = {"name":"name","network_type":"networkType"}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/infrastructure/networks",
    #    headers=headers,
    #    json=network_input,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_delete_network(client: TestClient):
    """Test case for delete_network

    Delete network
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/infrastructure/networks/{id}".format(id='id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_network(client: TestClient):
    """Test case for get_network

    Retrieve network
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/infrastructure/networks/{id}".format(id='id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_networks(client: TestClient):
    """Test case for get_networks

    Retrieve networks list
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/infrastructure/networks",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

