from pydantic import BaseModel
from typing import List

class AppConfig(BaseModel):
    env: str
    base_url: str
    base_path: str
    host: str
    port: int
    cors_origins: List[str]
    cors_methods: List[str]
    cors_headers: List[str]
    components: List[str]
    debug: bool
    api_prefix: str
    docs_url: str
    timeout: int