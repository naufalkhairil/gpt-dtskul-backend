from typing import List
from fastapi import APIRouter, UploadFile
from app.repositories.document import DocumentDep
from app.schemas.document import DocumentCreate, DocumentUpdate, DocumentResponse, UploadResponse

from app.config import Settings
config = Settings.get_settings()

router = APIRouter(prefix="/projects/{project_id}/documents", tags=["document"])

@router.post("/", response_model=DocumentResponse)
def create_new_document(
    project_id: int,
    document_data: DocumentCreate,
    documents: DocumentDep
):
    return documents.create_document(project_id, document_data)

@router.post("/upload", response_model=UploadResponse)
async def upload_documents(
    project_id: int,
    files: List[UploadFile],
    documents: DocumentDep
):    
    success, error = documents.upload_documents(project_id, files)
    return UploadResponse(
        success=success,
        error=error
    )

@router.get("/{document_id}", response_model=DocumentResponse)
def get_document_in_project(
    project_id: int,
    document_id: int,
    documents: DocumentDep
):    
    return documents.get_document(project_id, document_id)

@router.get("/", response_model=list[DocumentResponse])
def get_documents_in_project(
    project_id: int,
    documents: DocumentDep,
    skip: int = 0,
    limit: int = 10,
):    
    return documents.get_documents_in_project(project_id, skip, limit)

@router.get("/{document_id}/download")
def download_document_in_project(
    project_id: int,
    document_id: int,
    documents: DocumentDep,
):
    return documents.download_document(project_id, document_id)

@router.put("/{document_id}", response_model=DocumentResponse)
def update_document(
    project_id: int,
    document_id: int,
    document_data: DocumentUpdate,
    documents: DocumentDep
):    
    return documents.update_document(project_id, document_id, document_data)

@router.delete("/{document_id}")
def delete_document(
    project_id: int,
    document_id: int,
    documents: DocumentDep
):    
    document = documents.delete_document(project_id, document_id)
    return {"message": f"Document '{document.filename}' deleted successfully"}