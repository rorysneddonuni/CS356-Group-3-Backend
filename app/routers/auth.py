from fastapi import (
    APIRouter,
    Body,
    Depends,
    HTTPException,
)
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.config import RESET_TOKEN_LINK
from app.database.database import get_db
from app.models.error import Error
from app.models.login_request import LoginRequest
from app.models.login_response import LoginResponse
from app.services.auth import AuthService
from app.services.users import UsersService
from app.services.utility.email import EmailService

router = APIRouter()

class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

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

@router.post(
    "/auth/forgot-password",
    responses={
        200: {"description": "Reset link sent if email exists"},
        500: {"model": Error, "description": "Unexpected error"},
    },
    tags=["auth"],
    summary="Request password reset link",
)
async def forgot_password(
    data: ForgotPasswordRequest = Body(..., description="User email"),
    db: AsyncSession = Depends(get_db),
):
    user_service = UsersService()
    auth_service = AuthService()

    try:
        user = await user_service.get_user_by_email(str(data.email), db)
    except HTTPException:
        # Always return same message for security
        return {"message": "If an account exists, a reset link has been sent."}

    token = auth_service.create_reset_token(user.email)
    reset_link = f"{RESET_TOKEN_LINK}?token={token}"
    EmailService.send_reset_password_email(user.email, reset_link)

    return {"message": "If an account exists, a reset link has been sent."}


@router.post(
    "/auth/reset-password",
    responses={
        200: {"description": "Password reset successful"},
        400: {"description": "Invalid or expired token"},
        404: {"description": "User not found"},
        500: {"model": Error, "description": "Unexpected error"},
    },
    tags=["auth"],
    summary="Reset password using token",
)
async def reset_password(
    data: ResetPasswordRequest = Body(..., description="Token and new password"),
    db: AsyncSession = Depends(get_db),
):
    auth_service = AuthService()
    user_service = UsersService()

    email = auth_service.verify_reset_token(data.token)

    try:
        await user_service.get_user_by_email(email, db)
    except HTTPException:
        raise HTTPException(status_code=404, detail="User not found")

    hashed_password = auth_service.get_password_hash(data.new_password)
    await user_service.update_password(email=email, hashed_password=hashed_password, db=db)

    return {"message": "Password has been reset successfully"}