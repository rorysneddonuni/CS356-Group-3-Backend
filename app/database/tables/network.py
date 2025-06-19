from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.database import Base


class Network(Base):
    __tablename__ = "network"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=True)
    packet_loss = Column(Integer, nullable=True)
    delay = Column(Integer, nullable=True)
    jitter = Column(Integer, nullable=True)
    bandwidth = Column(Integer, nullable=True)

    experiments = relationship("Experiment", back_populates="network_disruption_profile")
