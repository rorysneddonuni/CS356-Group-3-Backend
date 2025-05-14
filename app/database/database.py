import os
from pathlib import Path
from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "backend.db"

DB_PATH.parent.mkdir(parents=True, exist_ok=True)

default_sqlite_url = f"sqlite:///{DB_PATH.as_posix()}"
DATABASE_URL = os.getenv("DATABASE_URL", default_sqlite_url)

engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


async def get_db():
    with Session() as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
