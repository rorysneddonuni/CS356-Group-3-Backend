from unittest.mock import patch, AsyncMock

from fastapi import status


class MockUser:
    def __init__(self, username="testuser", password="$2b$12$fakehashed", role="user"):
        self.username = username
        self.password = password
        self.role = role


@patch("app.routers.auth.AuthService.create_access_token", return_value="fake.jwt.token")
@patch("app.routers.auth.AuthService.verify_password", return_value=True)
@patch("app.services.users.SqliteUsersService.get_user_by_name", new_callable=AsyncMock)
def test_login_success(mock_get_user, mock_verify_password, mock_create_token, client, db):
    mock_user = MockUser()
    mock_get_user.return_value = mock_user

    response = client.post("/auth/login", json={"username": "testuser", "password": "correctpass"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["token"] == "fake.jwt.token"
    mock_create_token.assert_called_once()
    mock_verify_password.assert_called_once_with("correctpass", mock_user.password)


@patch("app.services.users.SqliteUsersService.get_user_by_name", new_callable=AsyncMock)
def test_login_invalid_user(mock_get_user, client, db):
    mock_get_user.return_value = None

    response = client.post("/auth/login", json={"username": "nouser", "password": "any"})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid username or password"


@patch("app.routers.auth.AuthService.verify_password", return_value=False)
@patch("app.services.users.SqliteUsersService.get_user_by_name", new_callable=AsyncMock)
def test_login_invalid_password(mock_get_user, mock_verify_password, client, db):
    mock_user = MockUser()
    mock_get_user.return_value = mock_user

    response = client.post("/auth/login", json={"username": "testuser", "password": "wrongpass"})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid username or password"
    mock_verify_password.assert_called_once()


@patch("app.routers.auth.AuthService.subclasses", [])
def test_login_not_implemented(client):
    response = client.post("/auth/login", json={"username": "any", "password": "irrelevant"})

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json()["detail"] == "Not implemented"