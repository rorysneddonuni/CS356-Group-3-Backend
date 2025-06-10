from sqlalchemy import Column, Integer, String, Boolean

from app.database.database import Base


class Encoders(Base):
    __tablename__ = "encoders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    encoder_type = Column(String)
    comment = Column(String)
    scalable = Column(Boolean, default=False)
    noOfLayers = Column(Integer)
    path = Column(String)
    filename = Column(String)
    modeFileReq = Column(Boolean, default=False)
    seqFileReq = Column(Boolean, default=False)
    layersFileReq = Column(Boolean, default=False)
