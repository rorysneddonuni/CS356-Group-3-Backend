from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import uuid4, UUID
from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, String

from app.database.database import Base, get_db

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# --- SQLAlchemy model ---
class User(Base):
    __tablename__ = "user"
    # store the UUID as a 36-char string in SQLite
    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    fullName = Column(String, nullable=False)
    lastName  = Column(String, nullable=False)
    password  = Column(String, nullable=False)
    email     = Column(String, unique=True, nullable=False)
    role      = Column(String, nullable=True)

# --- Pydantic schemas ---
class UserCreate(BaseModel):
    fullName: str
    lastName: str
    password: str
    email: EmailStr
    role: str | None = None

class UserRead(BaseModel):
    id: UUID
    fullName: str
    lastName: str
    email: EmailStr
    role: str | None = None

    class Config:
        from_attributes = True  # v2 rename of orm_mode

class UserUpdate(BaseModel):
    fullName: str | None = None
    lastName: str | None = None
    password: str | None = None
    email: EmailStr | None = None
    role: str | None = None

# --- CRUD routes ---
@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user_in.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    db_user = User(
        fullName=user_in.fullName,
        lastName=user_in.lastName,
        password=user_in.password,
        email=user_in.email,
        role=user_in.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/{user_id}", response_model=UserRead)
def read_user(user_id: UUID, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == str(user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.get("/", response_model=list[UserRead])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(User).offset(skip).limit(limit).all()

@router.put("/{user_id}", response_model=UserRead)
def update_user(user_id: UUID, user_in: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == str(user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    for field, value in user_in.dict(exclude_unset=True).items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == str(user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    db.delete(user)
    db.commit()
