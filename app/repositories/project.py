import os, shutil
from typing import List, Annotated
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.core.database import get_db
from app.models.user import UserModels, UserRole
from app.models.project import ProjectModels, ProjectAccessModels
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.utils import get_project_dir

from app.config import Settings
config = Settings.get_settings()

class ProjectRepo:
    def __init__(self, db: Session = Depends(get_db)):
        self.__db = db
    
    def check_project_access(self, project_id: int, user: UserModels):
        """Check if the user has access to the project, allowing superadmins full access"""
        if user.role == UserRole.SUPERADMIN:
            return  # Superadmins can access all projects

        access = self.__db.query(ProjectAccessModels).filter(
            ProjectAccessModels.project_id == project_id,
            ProjectAccessModels.user_id == user.id
        ).first()

        if not access:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this project")
    
    def create_project(self, project_data: ProjectCreate):
        if " " in project_data.name:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project name must not include space")
        
        os.makedirs(get_project_dir(project_data.name), exist_ok=True)

        new_project = ProjectModels(**project_data.model_dump())
        self.__db.add(new_project)
        self.__db.commit()
        self.__db.refresh(new_project)
        return new_project

    def get_project(self, project_id: int):
        project = self.__db.query(ProjectModels).filter(ProjectModels.id == project_id).first()
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    def get_all_projects(self, skip: int = 0, limit: int = 10):
        return self.__db.query(ProjectModels).offset(skip).limit(limit).all()

    def update_project(self, project_id: int, project_data: ProjectUpdate):
        project = self.__db.query(ProjectModels).filter(ProjectModels.id == project_id).first()
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

        project_path = get_project_dir(project.name)
        new_project_path = get_project_dir(project_data.name)

        for key, value in project_data.model_dump(exclude_unset=True).items():
            if key == "name":
                if not os.path.exists(project_path):
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
                
                os.rename(project_path, new_project_path)
                
            setattr(project, key, value)

        self.__db.commit()
        self.__db.refresh(project)
        return project

    def delete_project(self, project_id: int):
        project = self.__db.query(ProjectModels).filter(ProjectModels.id == project_id).first()
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        
        project_path = get_project_dir(project.name)
        if os.path.exists(project_path):
            shutil.rmtree(project_path)

        self.__db.delete(project)
        self.__db.commit()
        return project

ProjectDep = Annotated[ProjectRepo, Depends()]