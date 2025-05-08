import enum
from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func

from app.core.database import Base

class ProjectModels(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer)
    name = Column(String)
    description = Column(String)
    created_at = Column(DateTime, default=func.now(), onupdate=func.now())

class ProjectAccessLevel(str, enum.Enum):
    ADMIN = "admin"
    WRITE = "write"
    READ = "read"

class ProjectAccessModels(Base):
    __tablename__ = "project_access"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer)
    user_id = Column(Integer)
    access_level = Column(Enum(ProjectAccessLevel))
    granted_at = Column(DateTime, default=func.now(), onupdate=func.now())