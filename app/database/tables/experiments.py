from sqlalchemy import Column, Integer, String, JSON, Enum, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base
from app.models.experiment import ExperimentStatus


class Experiment(Base):
    """
    Experiment details
    """
    __tablename__ = "experiments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    experiment_name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(String(250), nullable=False)
    owner_id = Column(String(250), nullable=False)
    status = Column(Enum(ExperimentStatus))
    video_sources = Column(String(100))  # comma separated list
    encoding_parameters = Column(JSON, nullable=False)
    network_disruption_profile_id = Column(Integer, ForeignKey('network.id'))
    metrics_requested = Column(String(128))  # comma separated list
    progress = Column(String(250))
    created_at = Column(String(250))

    result_files = relationship("ExperimentResult", back_populates="experiment", cascade="all, delete-orphan", lazy="selectin")
    network_disruption_profile = relationship("Network", back_populates="experiments")
