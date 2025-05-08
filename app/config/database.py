from pydantic import BaseModel

class DatabaseConfig(BaseModel):
    url: str
    ssl_cert_file: str 
    ssl_key_file: str
    pool_size: int
    max_overflow: int
    pool_timeout: int