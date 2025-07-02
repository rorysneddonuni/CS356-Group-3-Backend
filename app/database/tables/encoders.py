from sqlalchemy import Column, Integer, String, Boolean

from app.database.database import Base


class Encoders(Base):
    __tablename__ = "encoders"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    encoder_type = Column(String)
    description = Column(String)
    scalable = Column(Boolean, default=False)
    maxLayers = Column(Integer)
    modeFileReq = Column(Boolean, default=False)
    seqFileReq = Column(Boolean, default=False)
    layersFileReq = Column(Boolean, default=False)
