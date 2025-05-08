from pathlib import Path
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from app.models.user import UserModels
from app.services.auth import get_current_user
from app.config import Settings

router = APIRouter(tags=["home"])

config = Settings.get_settings()
BASE_PATH = config.app.base_path
resources = Jinja2Templates(directory=str(Path(BASE_PATH, "frontend")))

@router.get("/", name="index")
async def index(
    request: Request,
    current_user: UserModels = Depends(get_current_user)
):

    return resources.TemplateResponse(
        "welcome.html",
        {
            "request": request,
            "base_url": request.base_url,
            "current_user": current_user,

        },
    )

@router.get("/logout")
async def logout():
    """Handle logout and clear session"""
    response = RedirectResponse(url="/login")
    response.delete_cookie("access_token")
    return response