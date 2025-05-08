import os
from typing import List, Annotated
from fastapi import Depends, HTTPException, UploadFile, File, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.project import ProjectModels
from app.models.document import DocumentModels
from app.schemas.document import DocumentCreate, DocumentUpdate
from app.utils import (
    get_root_project_dir,
    get_project_dir,
    get_relative_path
)

from app.config import Settings
config = Settings.get_settings()

class DocumentRepo:
    def __init__(self, db: Session = Depends(get_db)):  # ✅ Injects the DB session
        self.__db = db

    def create_document(self, project_id: int, document_data: DocumentCreate):
        project = self.__db.query(ProjectModels).filter(
            DocumentModels.project_id == project_id
        ).first()
        
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    
        new_document = DocumentModels(**document_data.model_dump())
        self.__db.add(new_document)
        self.__db.commit()
        self.__db.refresh(new_document)
        return new_document

    def get_document(self, project_id: int, document_id: int):
        project = self.__db.query(ProjectModels).filter(
            ProjectModels.id == project_id
        ).first()

        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        
        document = self.__db.query(DocumentModels).filter(
            DocumentModels.project_id == project_id,
            DocumentModels.id == document_id
        ).first()

        if not document:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

    def get_documents_in_project(self, project_id: int, skip: int = 0, limit: int = 10):
        project = self.__db.query(ProjectModels).filter(
            ProjectModels.id == project_id
        ).first()

        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        
        return self.__db.query(DocumentModels).filter(DocumentModels.project_id == project_id).offset(skip).limit(limit).all()

    def update_document(self, project_id: int, document_id: int, document_data: DocumentUpdate):
        project = self.__db.query(ProjectModels).filter(
            ProjectModels.id == project_id
        ).first()

        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        
        document = self.__db.query(DocumentModels).filter(
            DocumentModels.project_id == project_id,
            DocumentModels.id == document_id
        ).first()

        if not document:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

        for key, value in document_data.model_dump(exclude_unset=True).items():
            setattr(document, key, value)

        self.__db.commit()
        self.__db.refresh(document)
        return document

    def delete_document(self, project_id: int, document_id: int):
        project = self.__db.query(ProjectModels).filter(
            ProjectModels.id == project_id
        ).first()

        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        
        document = self.__db.query(DocumentModels).filter(
            DocumentModels.project_id == project_id,
            DocumentModels.id == document_id
        ).first()
        
        if not document:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

        document_abspath = os.path.join(get_root_project_dir(), document.file_url)
        if os.path.exists(document_abspath):
            os.remove(document_abspath)
            print("Deleted file: ", document_abspath)

        self.__db.delete(document)
        self.__db.commit()
        return document

    def download_document(self, project_id: int, document_id: int):
        project = self.__db.query(ProjectModels).filter(
            ProjectModels.id == project_id
        ).first()

        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

        document = self.__db.query(DocumentModels).filter(
            DocumentModels.project_id == project_id,
            DocumentModels.id == document_id
        ).first()

        project_dir = get_project_dir(project.name)
        document_path = os.path.join(project_dir, document.file_url)

        if not os.path.exists(document_path):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
        
        return FileResponse(document_path)
    
    def save_document(self, file: UploadFile, save_dir: str) -> str:
        file_location = os.path.join(save_dir, file.filename)

        if os.path.exists(file_location):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File with this name already exists")
        
        try:
            
            with open(file_location, "wb") as buffer:
                buffer.write(file.file.read())
            return file_location

        except OSError as e:
            # Handle OS-related errors (e.g., permission issues)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error saving file: {str(e)}")
        except Exception as e:
            # Handle any other exceptions
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {str(e)}")

    def upload_documents(self, project_id: int, files: List[UploadFile]):
        project = self.__db.query(ProjectModels).filter(
            ProjectModels.id == project_id
        ).first()

        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        
        success_documents = []
        error_documents = []
        for file in files:
            try:
                project_dir = get_project_dir(project.name)
                os.makedirs(project_dir, exist_ok=True)
                
                # file_location = self.save_document(file, project_dir)
                
                # Create a DocumentCreate instance
                new_document = self.create_document(DocumentCreate(
                    project_id=project.id,
                    filename=file.filename,
                    file_url=file.filename
                ))
                
                success_documents.append(new_document)
            except HTTPException as e:
                error_documents.append({
                    "filename": file.filename,
                    "message": e.detail,
                    "status": e.status_code,
                })
                continue
            except Exception as e:
                error_documents.append({
                    "filename": file.filename,
                    "message": str(e),
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                })
                continue
        
        # print("success", success_documents)
        # print("error", error_documents)
        
        return success_documents, error_documents

DocumentDep = Annotated[DocumentRepo, Depends()]