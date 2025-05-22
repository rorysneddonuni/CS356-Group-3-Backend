import shutil
import tempfile

import pytest
import pytest_asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.config.settings import Settings, get_settings
from app.database.database import Base, get_db
from app.main import app as application

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
TestingSessionLocal = async_sessionmaker(expire_on_commit=False, bind=engine, class_=AsyncSession)


@pytest_asyncio.fixture(scope="function")
async def db():
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as session:
        yield session  # provide the session to the test

    # Drop tables after test
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function", autouse=True)
def isolate_upload_dir(monkeypatch):
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def app(db, isolate_upload_dir) -> FastAPI:
    def override_get_db():
        yield db

    def override_get_settings():
        yield Settings(uploads_directory=isolate_upload_dir)

    application.dependency_overrides = {get_db: override_get_db, get_settings: override_get_settings}

    return application


@pytest.fixture
def client(app) -> TestClient:
    return TestClient(app)
