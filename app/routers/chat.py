from fastapi import APIRouter
from app.schemas.chat import Message
from app.services.message import message_service

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/message")
async def message(message: Message):
    return message_service.send(message)

@router.get("/suggestions")
async def get_suggestions():
    return message_service.get_suggestions()