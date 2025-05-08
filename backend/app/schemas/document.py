from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class DocumentCreate(BaseModel):
    project_id: int
    filename: str
    file_url: str

class DocumentUpdate(BaseModel):
    filename: Optional[str] = None
    file_url: Optional[str] = None

class DocumentResponse(BaseModel):
    id: int
    project_id: int
    filename: str
    file_url: str
    uploaded_at: datetime

    class Config:
        from_attributes = True

class DocumentError(BaseModel):
    filename: str
    message: str
    status: int

class UploadResponse(BaseModel):
    success: List[DocumentResponse]
    error: List[DocumentError]