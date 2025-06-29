from sqlalchemy import Column, Integer, String, Boolean

from app.database.database import Base


class Encoders(Base):
    __tablename__ = "encoders"

    id = Column(String, primary_key=True)
    video_id = Column(String(255), nullable=True)
    duration = Column(Integer, nullable=True)
    frames_to_encode = Column(Integer, nullable=True)
    fps = Column(Integer, nullable=True)
    res_width = Column(Integer, nullable=True)
    res_height = Column(Integer, nullable=True)
    input_file_title = Column(String(255), nullable=True)
    encoder = Column(String(255), nullable=True)
    encoder_type = Column(String(255), nullable=True)
    bit_rate = Column(Integer, nullable=True)
    yuv_format = Column(String(20), nullable=True)
    encoder_mode = Column(String(255), nullable=True)
    quality = Column(Integer, nullable=True)
    bit_depth = Column(Integer, nullable=True)
    infrared_period = Column(Integer, nullable=True)
    b_frames = Column(Integer, nullable=True)
    max_no_layers = Column(Integer, nullable=True)
