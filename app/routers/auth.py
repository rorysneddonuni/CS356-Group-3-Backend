from fastapi import (
    APIRouter,
    Body,
    Depends,
    HTTPException,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.models.error import Error
from app.models.login_request import LoginRequest
from app.models.login_response import LoginResponse
from app.services.auth import AuthService

router = APIRouter()

@router.post(
    "/auth/login",
    responses={
        200: {"model": LoginResponse, "description": "Login successful"},
        401: {"description": "Unauthorized - invalid credentials"},
        500: {"model": Error, "description": "Unexpected error"},
    },
    tags=["auth"],
    summary="User login (JSON payload)",
    response_model_by_alias=True,
)
async def login_user(
    login_request: LoginRequest = Body(..., description="User login credentials"),
    db: AsyncSession = Depends(get_db),
) -> LoginResponse:
    """Login via JSON (for Postman, frontend apps)"""
    if not AuthService.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await AuthService.subclasses[0]().login_user(login_request, db)