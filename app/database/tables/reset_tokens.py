from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base

class RefreshToken(Base):
    """
    Stores refresh tokens for user sessions.

    :id:         Unique identifier
    :token:      The opaque refresh token string
    :issued_at:  When this token was created
    :expires_at: When this token will expire
    :revoked:    Whether this token has been revoked
    """
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    token = Column(String, unique=True, index=True, nullable=False)
    issued_at = Column(DateTime, nullable=False)
    expires_at = Column(DateTime, nullable=False)

    # Link back to the user who owns this token
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="refresh_tokens")
