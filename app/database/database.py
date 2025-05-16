import os
from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "backend.db"

DB_PATH.parent.mkdir(parents=True, exist_ok=True)

default_sqlite_url = f"sqlite+aiosqlite:///{DB_PATH.as_posix()}"
DATABASE_URL = os.getenv("DATABASE_URL", default_sqlite_url)

engine = create_async_engine(
    DATABASE_URL,
    echo=True,    # set to False to disable SQL logging
    future=True,  # use SQLAlchemy 2.0 style
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session