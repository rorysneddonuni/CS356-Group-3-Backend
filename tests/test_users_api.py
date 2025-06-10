from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.user import User
from app.routers import users

mock_user = User(id=1, username="testuser", role="super_admin", email="test@example.com")

async def override_get_db():
    yield MagicMock()

def override_get_current_user():
    return mock_user

def override_require_minimum_role(role):
    def dependency():
        return mock_user
    return dependency

def override_has_access_to_user(user, username):
    return True

class MockUserService:
    async def create_user(self, data, db): return mock_user
    async def get_user_by_name(self, username, db): return mock_user
    async def get_all_users(self, db, roles=None): return [mock_user]
    async def update_user(self, username, data, db): return mock_user
    async def delete_user(self, username, db): return None

@pytest.fixture(autouse=True, scope="module")
def test_app():
    app.dependency_overrides[users.get_db] = override_get_db
    app.dependency_overrides[users.get_current_user] = override_get_current_user
    app.dependency_overrides[users.require_minimum_role] = override_require_minimum_role

    users.UsersService.subclasses = [MockUserService]

    yield TestClient(app)

    app.dependency_overrides = {}
    users.UsersService.subclasses = []

def test_get_all_users(test_app):
    response = test_app.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_user_by_username(test_app):
    response = test_app.get("/users/testuser")
    assert response.status_code == 200


def test_update_user(test_app):
    response = test_app.put("/users/testuser", json={"email": "updated@example.com"})
    assert response.status_code == 200


def test_delete_user(test_app):
    response = test_app.delete("/users/testuser")
    assert response.status_code == 200

