from sqlalchemy import Column, Integer, String, Enum
import enum

from app.database.database import Base

class UserRole(enum.Enum):
    user = "user"
    admin = "admin"
    superadmin = "superadmin"


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(128), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.user)
