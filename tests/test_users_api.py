import pytest
from httpx import AsyncClient
from app.models.user_input import UserInput
from app.services.users import UsersService

from app.models.user import User
from app.routers.users import get_current_user


@pytest.mark.asyncio
class TestUserRoutes:

    async def test_create_user(self, async_client: AsyncClient):
        new_user_data = {
            "username": "newuser",
            "first_name": "New",
            "last_name": "User",
            "email": "newuser@example.com",
            "password": "secret",
            "role": "user"
        }

        response = await async_client.post("/users", json=new_user_data)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "newuser"
        assert data["firstName"] == "New"
        assert data["role"] == "user"

    async def test_get_all_users_as_user(self, async_client: AsyncClient, test_user_input: UserInput):
        await async_client.post("/users", json={
            "username": test_user_input.username,
            "first_name": test_user_input.first_name,
            "last_name": test_user_input.last_name,
            "email": test_user_input.email,
            "password": test_user_input.password,
            "role": "user"
        })

        response = await async_client.get("/users")
        assert response.status_code == 200
        users = response.json()
        assert isinstance(users, list)
        assert any(u["username"] == test_user_input.username for u in users)

    async def test_get_user_by_username(self, async_client: AsyncClient, user_factory):
        await user_factory(username="testuser", role="user")

        response = await async_client.get("/users/testuser")
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "testuser@example.com"

    async def test_update_user(self, async_client: AsyncClient, test_user_input: UserInput):
        await async_client.post("/users", json={
            "username": test_user_input.username,
            "first_name": test_user_input.first_name,
            "last_name": test_user_input.last_name,
            "email": test_user_input.email,
            "password": test_user_input.password,
            "role": "user"
        })

        update_data = {
            "first_name": "Updated",
            "last_name": "Name",
            "email": "updated@example.com"
        }

        response = await async_client.put(f"/users/{test_user_input.username}", json=update_data)
        assert response.status_code == 200
        updated = response.json()
        assert updated["firstName"] == "Updated"
        assert updated["lastName"] == "Name"
        assert updated["email"] == "updated@example.com"

    async def test_delete_user(self, async_client: AsyncClient, db):
        user_to_delete = UserInput(
            username="deleteuser",
            first_name="Delete",
            last_name="Me",
            email="delete@example.com",
            password="testpass"
        )
        await UsersService.subclasses[0]().create_user(user_to_delete, db)

        response = await async_client.delete(f"/users/{user_to_delete.username}")
        assert response.status_code == 200

    async def test_get_user_unauthorized_access(self, async_client: AsyncClient, app):
        fake_user = User(username="notowner", role="user")

        async def fake_current_user():
            return fake_user

        app.dependency_overrides[get_current_user] = fake_current_user

        response = await async_client.get("/users/unauthorized")
        assert response.status_code == 401

        app.dependency_overrides.clear()
