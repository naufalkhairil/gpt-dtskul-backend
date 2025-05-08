from pydantic import BaseModel

class GPTConfig(BaseModel):
    url: str
    api_key: str
    model: str
