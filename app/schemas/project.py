from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class ProjectCreate(BaseModel):
    owner_id: int
    name: str
    description: Optional[str] = None

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class ProjectResponse(BaseModel):
    id: int
    owner_id: int
    name: str
    description: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True