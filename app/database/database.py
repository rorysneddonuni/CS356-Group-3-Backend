import os
from pathlib import Path
from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "backend.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

default_sqlite_url = f"sqlite+aiosqlite:///{DB_PATH.as_posix()}"
DATABASE_URL = os.getenv("DATABASE_URL", default_sqlite_url)

engine = create_async_engine(DATABASE_URL, echo=True)

Session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with Session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_db)]