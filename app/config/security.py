from pydantic import BaseModel

class SecurityConfig(BaseModel):
    jwt_secret: str
    algorithm: str
    access_token_expire_minutes: int
