import os
from app.config import Settings
config = Settings.get_settings()

def get_root_project_dir():
    try:
        return config.project.path
    except:
        return "./project_storage"

def init_root_project_dir():
    root_dir = get_root_project_dir()
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)

def get_project_dir(project_name: str):
    return os.path.join(get_root_project_dir(), project_name)

def get_relative_path(target_file: str, base_directory: str) -> str:
    base_directory = os.path.abspath(base_directory)
    relative_path = os.path.relpath(target_file, base_directory)
    
    return relative_path