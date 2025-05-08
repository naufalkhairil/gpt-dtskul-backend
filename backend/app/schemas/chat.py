from pydantic import BaseModel
from typing import List

class Message(BaseModel):
    content: str
    is_user: bool = True

class ChatHistory(BaseModel):
    messages: List[Message]