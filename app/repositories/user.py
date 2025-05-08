import enum
from typing import List
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core import security
from app.core.database import get_db
from app.models.user import UserModels, UserRole
from app.schemas.user import UserCreate, UserUpdate

class UserRepo:
    def __init__(self, db: Session = Depends(get_db)):
        self.__db = db
    
    def create_user(self, user_data: UserCreate):
        existing_user = self.__db.query(UserModels).filter(
            (UserModels.email == user_data.email) | (UserModels.username == user_data.username)
        ).first()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email or username already exists")

        hashed_password = security.get_password_hash(user_data.password)

        new_user = UserModels(
            email = user_data.email,
            username = user_data.username,
            hashed_password = hashed_password,
            role = user_data.role,
            is_active = True,
            status = 1, 
        )
        self.__db.add(new_user)
        self.__db.commit()
        self.__db.refresh(new_user)
        return new_user

    def create_user_with_role(self, user_data: UserCreate, role: enum.Enum):

        if (
            user_data.role == UserRole.SUPERADMIN and
            role != UserRole.SUPERADMIN
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only superadmin can create other superadmins"
            )
        
        return self.create_user(user_data)
    
    def get_user_by_id(self, user_id: int):
        user = self.__db.query(UserModels).filter(UserModels.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

            
        return user

    def get_user_by_email(self, email: str):
        user = self.__db.query(UserModels).filter(UserModels.email == email).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        
        return user

    def get_user_by_username(self, username: str):
        user = self.__db.query(UserModels).filter(UserModels.username == username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        
        return user

    def get_all_users(self, skip: int = 0, limit: int = 100):
        return self.__db.query(UserModels).offset(skip).limit(limit).all()

    def update_user(self, user_id: int, user_data: UserUpdate):
        user = self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        
        for key, value in user_data.model_dump(exclude_unset=True).items():
            if key == "password":
                hashed_password = security.get_password_hash(value)
                setattr(user, key, hashed_password)
            else:
                setattr(user, key, value)

        self.__db.commit()
        self.__db.refresh(user)
        return user

    def update_user_with_role(self, user_id: int, user_data: UserUpdate, role: enum.Enum):
        if user_data.role:
            if (
                user_data.role == UserRole.SUPERADMIN and
                role != UserRole.SUPERADMIN
            ):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Only superadmin can assign superadmin role"
                )
        
        return self.update_user(user_id, user_data)

    def delete_user(self, user_id: int) -> dict:
        user = self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


        self.__db.delete(user)
        self.__db.commit()
        return {"message": f"User {user.username} deleted successfully"}
    
    def delete_user_with_role(self, user_id: int, role: enum.Enum) -> dict:
        user = self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        
        if (
            user.role == UserRole.SUPERADMIN and
            role != UserRole.SUPERADMIN
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only superadmin can delete superadmins",
            )
        
        return self.delete_user(user_id)
    


    
        