from datetime import datetime

from sqlalchemy import Column, Integer, String

from app.database.database import Base


class InputVideo(Base):
    """
    Location of result files for a given parent experiment.

    :id: Unique identifier
    :filename: Filename passed by the user and that which shall be returned
    :path: The path of where this file is stored on system (actual filename will have been modified to avoid conflict)
    """
    __tablename__ = "input_videos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    groupId = Column(Integer)
    title = Column(String, nullable=False)
    path = Column(String)
    format = Column(String)
    frameRate = Column(Integer)
    res = Column(String)
    lastUpdated = Column(String)
    description = Column(String)
    bitDepth = Column(Integer)
