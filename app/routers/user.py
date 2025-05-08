from datetime import timedelta
from typing import List
from fastapi import APIRouter, Response, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from app.core import security
from app.repositories.user import UserRepo
from app.models.user import UserModels
from app.schemas.user import User, UserCreate, UserUpdate, UserResponse, UserToken
from app.services.auth import check_admin_access, get_current_user

from app.config import Settings
config = Settings.get_settings()

router = APIRouter(prefix="/users", tags=["user"])

@router.post("/token", response_model=UserToken)
async def user_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_repo: UserRepo = Depends()
):
    user = user_repo.get_user_by_username(form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    print("access token", access_token)
    response.set_cookie(
        key="token_cookie",
        value=access_token,
        httponly=True,
        samesite="Lax",
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    user_repo: UserRepo = Depends(),
):  
    return user_repo.create_user(user)

@router.get("/user/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: int,
    user_repo: UserRepo = Depends(),
):
    return user_repo.get_user_by_id(user_id)

@router.get("/", response_model=List[UserResponse])
async def get_all_users(
    user_repo: UserRepo = Depends(),
    skip: int = 0,
    limit: int = 100,
):
    return user_repo.get_all_users(skip, limit)

@router.get("/me", response_model=UserResponse)
async def get_user_me(
    current_user: UserModels = Depends(get_current_user)
):
    return current_user

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    user_repo: UserRepo = Depends(),
    _: User = Depends(check_admin_access),
):
    return user_repo.update_user(
        user_id = user_id,
        user_data = user_update
    )

@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    user_repo: UserRepo = Depends(),
    _: User = Depends(check_admin_access),
):
    Depends(check_admin_access)
    return user_repo.delete_user(
        user_id = user_id,
    )