import yaml, os
from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache
from .app import AppConfig
from .log import LoggingConfig
from .security import SecurityConfig
from .database import DatabaseConfig
from .gpt import GPTConfig
from .project import ProjectConfig

DEFAULT_SETTINGS_NAME = "config.yaml"
DEFAULT_SETTINGS_PATH = f"../{DEFAULT_SETTINGS_NAME}"

class Settings(BaseSettings):
    app: AppConfig
    logging: LoggingConfig
    security: SecurityConfig
    database: DatabaseConfig
    gpt: GPTConfig
    project: Optional[ProjectConfig] = None

    @staticmethod
    def check_yaml_path() -> str:
        run_dir_settings = os.path.join(os.getcwd(), DEFAULT_SETTINGS_NAME)
        if os.path.exists(run_dir_settings):
            return run_dir_settings
        elif os.path.exists(DEFAULT_SETTINGS_PATH):
            return DEFAULT_SETTINGS_PATH
        else:
            raise FileNotFoundError("Settings file not found")

    @classmethod
    @lru_cache
    def get_settings(cls) -> "Settings":
        yaml_path = cls.check_yaml_path()
        with open(yaml_path, 'r') as f:
            config_data = yaml.safe_load(f)
        return cls(**config_data)
        
settings = Settings.get_settings()
