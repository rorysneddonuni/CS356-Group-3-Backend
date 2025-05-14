from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class Experiment(Base):
    """
    Experiment details
    """
    __tablename__ = "experiments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(String(250), nullable=False)
    owner_id = Column(String(250), nullable=False)
    status = Column(String(250), nullable=False)
    video_sources = Column(String(100))  # comma separated list
    codec = Column(String(100), unique=True, nullable=False, index=True)
    bitrate = Column(String(100), unique=True, nullable=False, index=True)
    resolution = Column(String(100), unique=True, nullable=False, index=True)
    network_conditions = Column(String(128))
    metrics_requested = Column(String(128))  # comma separated list
    progress = Column(String(250))
    created_at = Column(String(250))

    result_files = relationship("ExperimentResult", back_populates="experiment", cascade="all, delete-orphan")


class ExperimentResult(Base):
    """
    Location of result files for a given parent experiment.

    :id: Unique identifier
    :filename: Filename passed by the user and that which shall be returned
    :path: The path of where this file is stored on system (actual filename will have been modified to avoid conflict)
    """
    __tablename__ = "experiments_results"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    filename = Column(String, nullable=False)
    path = Column(String)

    experiment_id = Column(Integer, ForeignKey("experiments.id"), nullable=False)
    experiment = relationship("Experiment", back_populates="result_files")
