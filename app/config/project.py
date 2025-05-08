from typing import Optional
from pydantic import BaseModel

class ProjectConfig(BaseModel):
    path: Optional[str] = "./project_storage"
