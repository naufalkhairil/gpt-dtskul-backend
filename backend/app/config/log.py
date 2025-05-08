from pydantic import BaseModel

class LoggingConfig(BaseModel):
    level: str = "DEBUG"
    filename: str
    format: str