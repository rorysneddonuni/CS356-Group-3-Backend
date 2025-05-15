import shutil
import tempfile

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.settings import Settings, get_settings
from app.database.database import Base, get_db
from app.main import app as application

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


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
