import pytest
from httpx import AsyncClient
from app.services.auth import AuthService


@pytest.mark.asyncio
class TestAuthRoutes:

    async def test_login_success(self, async_client: AsyncClient, user_factory):
        await user_factory(username="loginuser", password="validpass")

        response = await async_client.post("/auth/login", json={
            "username": "loginuser",
            "password": "validpass"
        })

        assert response.status_code == 200
        assert "token" in response.json()

    async def test_login_failure_invalid_credentials(self, async_client: AsyncClient, user_factory):
        await user_factory(username="wronglogin", password="correctpass")

        response = await async_client.post("/auth/login", json={
            "username": "wronglogin",
            "password": "wrongpass"
        })

        assert response.status_code == 401
        assert "invalid username or password" in response.text.lower()

    async def test_forgot_password_existing_user(self, async_client: AsyncClient, user_factory):
        await user_factory(username="forgotuser", email="forgot@example.com")

        response = await async_client.post("/auth/forgot-password", json={
            "email": "forgot@example.com"
        })

        assert response.status_code == 200
        assert "reset link" in response.json()["message"].lower()

    async def test_forgot_password_nonexistent_user(self, async_client: AsyncClient):
        response = await async_client.post("/auth/forgot-password", json={
            "email": "ghost@example.com"
        })

        assert response.status_code == 200
        assert "reset link" in response.json()["message"].lower()

    async def test_reset_password_success(self, async_client: AsyncClient, user_factory):
        email = "resetme@example.com"
        await user_factory(username="resetme", password="oldpass", email=email)

        new_password = "NewStrongPass123"
        token = AuthService().create_reset_token(email)

        response = await async_client.post("/auth/reset-password", json={
            "token": token,
            "new_password": new_password
        })

        assert response.status_code == 200
        assert "reset successfully" in response.json()["message"]

        login_response = await async_client.post("/auth/login", json={
            "username": "resetme",
            "password": new_password
        })

        assert login_response.status_code == 200
        assert "token" in login_response.json()

    async def test_reset_password_invalid_token(self, async_client: AsyncClient):
        response = await async_client.post("/auth/reset-password", json={
            "token": "invalid.token.value",
            "new_password": "whatever123"
        })

        assert response.status_code == 400
        assert "invalid or expired token" in response.text.lower()

    async def test_reset_password_user_not_found(self, async_client: AsyncClient):
        fake_email = "ghost@example.com"
        token = AuthService().create_reset_token(fake_email)

        response = await async_client.post("/auth/reset-password", json={
            "token": token,
            "new_password": "NewPassword123!"
        })

        assert response.status_code == 404
        assert "user not found" in response.text.lower()
