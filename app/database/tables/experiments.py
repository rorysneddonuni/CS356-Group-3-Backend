from sqlalchemy import Column, Integer, String, JSON, Enum, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base
from app.models.experiment import ExperimentStatus


class ExperimentSequence(Base):
    """
    Individual sets/sequences of an experiment
    """
    __tablename__ = "experiment_sequences"

    sequence_id = Column(Integer, primary_key=True, autoincrement=True)
    parent_experiment_id = Column(Integer, ForeignKey('experiments.id'))
    network_topology_id = Column(Integer, ForeignKey('network.network_profile_id'))
    network_disruption_profile_id = Column(Integer, ForeignKey('network.network_profile_id'))
    encoding_parameters = Column(JSON)

    network_disruption_profile = relationship("Network", foreign_keys=[network_disruption_profile_id], back_populates="network_disruption_profile_sequences")
    network_topology = relationship("Network", foreign_keys=[network_topology_id], back_populates="network_topology_sequences")
    experiment = relationship("Experiment", back_populates="sequences")


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
    created_at = Column(String(250))

    result_files = relationship("ExperimentResult", back_populates="experiment", cascade="all, delete-orphan", lazy="selectin")
    sequences = relationship("ExperimentSequence", back_populates="experiment")
