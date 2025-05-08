from datetime import timedelta
from pathlib import Path
from fastapi import APIRouter, Response, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.models.user import UserModels
from app.repositories.user import UserRepo
from app.services.auth import get_current_user
from app.core import security

from app.config import Settings
config = Settings.get_settings()
BASE_PATH = config.app.base_path
resources = Jinja2Templates(directory=str(Path(BASE_PATH, "frontend")))

router = APIRouter(prefix="/login", tags=["login"])

@router.get("/")
async def login_page(request: Request):
    """Render the login page"""
    return resources.TemplateResponse(
        "user/login.html", {"request": request, "base_url": request.base_url}
    )

@router.post("/api/access-token")
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_repo: UserRepo = Depends(),
):
    """Handle login authentication and return JWT token"""
    user = user_repo.get_user_by_username(form_data.username)

    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    response = JSONResponse(content={"access_token": access_token, "token_type": "bearer"})
    # Set cookie with token
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=1800,  # 30 minutes
        expires=1800,
        samesite="lax",
        # secure=True  # Set to True if using HTTPS
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
        },
    }


@router.post("/api/verify-token")
async def verify_token(current_user: UserModels = Depends(get_current_user)):
    """Verify if the current token is valid"""
    return {
        "valid": True,
        "user": {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "role": current_user.role,
        },
    }