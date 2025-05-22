from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Encoder(Base):
    __tablename__ = "encoder"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    encoder_type = Column(String(50), nullable=False)
    encoder_code = Column(String(255), nullable=False)
    layers = Column(JSON, nullable=False)  # stores list of strings