from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Integer, String, Enum
from sqlalchemy.orm import relationship
import enum

from app.database.database import Base

class UserRole(enum.Enum):
    pending = "pending"
    user = "user"
    admin = "admin"
    super_admin = "super_admin"


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(128), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.pending)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    refresh_tokens = relationship(
        "RefreshToken",
        back_populates="user",
        cascade="all, delete-orphan"
    )


