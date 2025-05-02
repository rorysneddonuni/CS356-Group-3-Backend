from fastapi.testclient import TestClient


from pydantic import Field, StrictStr  # noqa: F401
from typing import Any, Optional  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from app.models.error import Error  # noqa: F401
from app.models.user import User  # noqa: F401
from app.models.user_input import UserInput  # noqa: F401


def test_create_user(client: TestClient):
    """Test case for create_user

    Create a user.
    """
    user_input = {"first_name":"John","last_name":"James","password":"12345","email":"john@email.com","username":"theUser"}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/users",
    #    headers=headers,
    #    json=user_input,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_delete_user(client: TestClient):
    """Test case for delete_user

    Delete user resource.
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/users/{username}".format(username='username_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_user_by_name(client: TestClient):
    """Test case for get_user_by_name

    Get user by username.
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/users/{username}".format(username='username_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_update_user(client: TestClient):
    """Test case for update_user

    Update user resource.
    """
    user_input = {"first_name":"John","last_name":"James","password":"12345","email":"john@email.com","username":"theUser"}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/users/{username}".format(username='username_example'),
    #    headers=headers,
    #    json=user_input,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

