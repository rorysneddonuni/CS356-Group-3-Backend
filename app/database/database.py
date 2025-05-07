import os
import sqlite3
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine

# file-based SQLite (no external server)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./backend.db")

# turn off check_same_thread so FastAPI can share the connection
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# enforce foreign-keys if you add relationships later
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
