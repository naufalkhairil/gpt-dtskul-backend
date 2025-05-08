from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.core.database import Base

class DocumentModels(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer)
    filename = Column(String)
    file_url = Column(String)
    uploaded_at = Column(DateTime, default=func.now(), onupdate=func.now())