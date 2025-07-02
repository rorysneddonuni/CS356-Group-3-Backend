import shutil
import tempfile
from datetime import datetime
from io import BytesIO

import pytest
import pytest_asyncio
from fastapi import FastAPI, UploadFile
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.auth.dependencies import user_dependency, super_admin_dependency, get_current_user
from app.config.settings import Settings, get_settings
from app.database.database import Base, get_db
from app.main import app as application
from app.models.encoder_input import EncoderInput
from app.models.experiment import Experiment, ExperimentStatus
from app.models.network import NetworkInput
from app.models.user import User
from app.models.user_input import UserInput
from app.services.encoders import EncodersService
from app.services.networks import NetworksService
from app.services.videos import VideosService

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=False)
TestingSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

@pytest_asyncio.fixture(scope="function")
async def db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with TestingSessionLocal() as session:
        yield session
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="function", autouse=True)
def isolate_upload_dir(monkeypatch):
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def app(db, isolate_upload_dir) -> FastAPI:
    async def override_get_db():
        yield db

    async def override_get_settings():
        yield Settings(uploads_directory=isolate_upload_dir)

    application.dependency_overrides[get_db] = override_get_db
    application.dependency_overrides[get_settings] = override_get_settings
    return application

@pytest_asyncio.fixture
async def async_client(app: FastAPI) -> AsyncClient:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


# --- User ---
@pytest.fixture
def test_user_input() -> UserInput:
    return UserInput(
        username="testuser",
        first_name="Test",
        last_name="User",
        email="test@example.com",
        password="securepassword"
    )

@pytest.fixture
def test_super_admin_input() -> UserInput:
    return UserInput(
        username="admin",
        first_name="Super",
        last_name="Admin",
        email="admin@example.com",
        password="adminpassword",
        role="super_admin"
    )

@pytest.fixture
def test_user(test_user_input: UserInput) -> User:
    return User(
        id=1,
        username=test_user_input.username,
        first_name=test_user_input.first_name,
        last_name=test_user_input.last_name,
        email=test_user_input.email,
        role="user"
    )

@pytest.fixture
def test_super_admin(test_super_admin_input: UserInput) -> User:
    return User(
        id=2,
        username=test_super_admin_input.username,
        first_name=test_super_admin_input.first_name,
        last_name=test_super_admin_input.last_name,
        email=test_super_admin_input.email,
        role="super_admin"
    )

@pytest.fixture(autouse=True)
def override_user_dependencies(app, test_user):
    async def _mock_get_current_user():
        return test_user

    app.dependency_overrides[get_current_user] = _mock_get_current_user
    yield
    app.dependency_overrides.clear()

@pytest.fixture(autouse=True)
def override_role_dependencies(app, test_user, test_super_admin):
    app.dependency_overrides[user_dependency] = lambda: test_user
    app.dependency_overrides[super_admin_dependency] = lambda: test_super_admin
    yield
    app.dependency_overrides.clear()

@pytest.fixture
def user_factory(async_client: AsyncClient):
    created_users = set()

    async def _create_user(username="testuser", password="secret", role="user", email=None):
        if username in created_users:
            return  # Avoid re-creating same user

        user_data = {
            "username": username,
            "first_name": username.capitalize(),
            "last_name": "User",
            "email": email or f"{username}@example.com",
            "password": password,
            "role": role
        }

        response = await async_client.post("/users", json=user_data)
        assert response.status_code == 200
        created_users.add(username)
        return user_data

    return _create_user

# --- Encoder ---
@pytest.fixture
def test_encoder_json():
    return {
        "id": 101,
        "name": "Test Encoder",
        "encoderType": "h264",
        "comment": "Test encoder entry",
        "scalable": False,
        "noOfLayers": 1,
        "path": "/usr/bin/encoder",
        "filename": "encoder.exe",
        "modeFileReq": False,
        "seqFileReq": False,
        "layersFileReq": False
    }

@pytest.fixture
def encoder_factory(db: AsyncSession):
    async def _create_encoder(data: dict):
        encoder_input = EncoderInput(**data)
        return await EncodersService().create_encoder(encoder_input, db)
    return _create_encoder


# --- Experiments ---
@pytest.fixture
def experiment_input_payload():
    return {
        "ExperimentName": "Test Exp",
        "Description": "Test description",
        "Status": "PENDING",
        "Sequences": [
            {
                "NetworkTopologyId": 1,
                "NetworkDisruptionProfileId": 2,
                "EncodingParameters": {"codec": "h264"}
            }
        ]
    }

@pytest.fixture
def experiment_update_payload():
    return {
        "ExperimentName": "Updated Exp",
        "Description": "Updated desc",
        "Status": "COMPLETE",
        "AddSequences": [],
        "RemoveSequenceIds": []
    }

@pytest.fixture
def experiment(db):
    async def _create_experiment():
        exp = Experiment(
            id=9000,
            experiment_name="UploadTest",
            description="Test upload results",
            owner_id=1,
            status=ExperimentStatus.COMPLETE,
            created_at=datetime.now()
        )
        db.add(exp)
        await db.commit()
        await db.refresh(exp)
        return exp

    return _create_experiment


# --- Network ---
@pytest.fixture
def test_network_json():
    return {
        "networkName": "Test Network",
        "description": "Initial description",
        "packetLoss": 1,
        "delay": 20,
        "jitter": 5,
        "bandwidth": 1000
    }

@pytest.fixture
def network_factory(db: AsyncSession):
    async def _create_network(data: dict):
        input_model = NetworkInput(**data)
        return await NetworksService().create_network(input_model, db)
    return _create_network


# --- Videos ---
@pytest.fixture
def test_video_data():
    return {
        "title": "sample_video",
        "format": "y4m",
        "frameRate": 30,
        "resolution": "1920x1080",
        "description": "Test video upload",
        "bitDepth": 8,
    }

@pytest.fixture
def video_factory(db, test_super_admin):
    async def _create_video(**kwargs):
        file = UploadFile(filename="video.y4m", file=BytesIO(b"YUV4MPEG2 content"))
        return await VideosService().create_video(
            video=file,
            current_user=test_super_admin,
            db=db,
            **kwargs
        )
    return _create_video

# --- Results ---

@pytest.fixture(autouse=True)
def override_user_dep(app):
    mock_user = User(
        id=1,
        username="testuser",
        password="fake",
        role="user",
        email="test@example.com",
        first_name="Test",
        last_name="User"
    )
    app.dependency_overrides[user_dependency] = lambda: mock_user


@pytest_asyncio.fixture
async def create_experiment(db):
    async def _create():
        exp = Experiment(
            experiment_name="UploadTest",
            description="Test upload results",
            owner_id=1,
            status=ExperimentStatus.COMPLETE,
            created_at=datetime.now().isoformat()
        )
        db.add(exp)
        await db.commit()
        await db.refresh(exp)
        return exp
    return _create
