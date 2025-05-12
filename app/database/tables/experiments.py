from sqlalchemy import Column, Integer, String
from app.database.database import Base

class ExperimentsTable(Base):
    __tablename__ = "experiments"

    id         = Column(Integer, primary_key=True, index=True, autoincrement=True)
    experiment_name   = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(String(250), nullable=False)
    owner_id = Column(String(250), nullable=False)
    status = Column(String(250), nullable=False)
    video_sources  = Column(String(100), nullable=False)  # comma separated list
    results_location =Column(String(100), nullable=False)
    codec      = Column(String(100), unique=True, nullable=False, index=True)
    bitrate      = Column(String(100), unique=True, nullable=False, index=True)
    resolution    = Column(String(100), unique=True, nullable=False, index=True)
    network_conditions   = Column(String(128), nullable=False)
    metrics_requested   = Column(String(128), nullable=False) # comma separated list
    progress = Column(String(250), nullable=False)
    created_at = Column(String(250), nullable=False)
