from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.templating import Jinja2Templates
from app.repositories.project import ProjectDep
from app.models.user import UserModels
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from app.services.auth import check_admin_access

from app.config import Settings
config = Settings.get_settings()
BASE_PATH = config.app.base_path
resources = Jinja2Templates(directory=str(Path(BASE_PATH, "frontend")))

router = APIRouter(prefix="/projects", tags=["project"])

@router.get("/page")
async def project_page(request: Request):
    return resources.TemplateResponse(
        "user/project.html", {"request": request, "base_url": request.base_url}
    )

@router.post("/", response_model=ProjectResponse)
def create_new_project(
    project_data: ProjectCreate,
    projects: ProjectDep,
):
    return projects.create_project(project_data)

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project_by_id(
    project_id: int,
    projects: ProjectDep,
):
    return projects.get_project(project_id)

@router.get("/", response_model=list[ProjectResponse])
def get_all_projects_list(
    projects: ProjectDep,
    skip: int = 0,
    limit: int = 10,
):
    return projects.get_all_projects(skip, limit)

@router.put("/{project_id}", response_model=ProjectResponse)
def update_existing_project(
    project_id: int, 
    project_data: ProjectUpdate,
    projects: ProjectDep,
    current_user: UserModels = Depends(check_admin_access),
):
    projects.check_project_access(project_id, current_user)
    return projects.update_project(project_id, project_data)

@router.delete("/{project_id}")
def delete_existing_project(
    project_id: int,
    projects: ProjectDep,
    current_user: UserModels = Depends(check_admin_access),
):
    projects.check_project_access(project_id, current_user)
    project = projects.delete_project(project_id)
    return {"message": f"Project {project.name} deleted successfully"}