from jose import JWTError, jwt
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, Cookie
from fastapi.security import OAuth2PasswordBearer
from app.models.user import UserModels, UserRole
from app.repositories.user import UserRepo
from app.core.database import get_db
from app.config import Settings
config = Settings.get_settings()

# async def get_current_user_regular(token: str, db: Session):
#     """Check user credentials based on provided token and database session"""
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials, please login to " + config.app.base_url + 'user_manager/login',
#         headers={"WWW-Authenticate": "Bearer","Location":config.app.base_url},
#     )
#     try:
#         payload = jwt.decode(token, config.security.jwt_secret, algorithms=[config.security.algorithm])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception
    
#     user = db.query(UserModels).filter(UserModels.username == username).first()
#     if user is None:
#         raise credentials_exception
#     return user

async def get_token_from_cookie(token_cookie: str = Cookie(None)):
    if token_cookie:
        return token_cookie
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated, try a login first")

async def get_current_user(
        token: str = Depends(get_token_from_cookie),
        user_repo: UserRepo = Depends()
):
    print("token", token)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials, please login",
        headers={"WWW-Authenticate": "Bearer","Location": config.app.base_url},
    )
    try:
        payload = jwt.decode(token, config.security.jwt_secret, algorithms=[config.security.algorithm])
        username: str = payload.get("sub")
        if username is None:
            print("Username not found in token.")
            raise credentials_exception
        print(f"Token payload: {payload}")  # Debugging line
    except JWTError as e:
        print(f"JWTError: {str(e)}")  # Debugging line
        raise credentials_exception
    
    user = user_repo.get_user_by_username(username)
    if user is None:
        print(f"User with username '{username}' not found.")
        raise credentials_exception
    else:
        print(f"User found: {user}")
    return user

def check_admin_access(current_user: UserModels = Depends(get_current_user)):
    if current_user.role not in [UserRole.ADMIN, UserRole.SUPERADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user

def check_superadmin_access(current_user: UserModels = Depends(get_current_user)):
    if current_user.role != UserRole.SUPERADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user
