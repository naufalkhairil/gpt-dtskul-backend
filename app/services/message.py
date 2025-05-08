from groq import Groq
from app.schemas.chat import Message
from app.config import Settings
import requests
config = Settings.get_settings()

class MessageService:
    def __init__(self):
        self.__chat_histories = {}
        self.__model = "llama-3.3-70b-instant"
    
    def send(self, message: Message) -> Message:
        if message.content.strip().lower() == "siapakah nama pemilik akun ini?":
            return Message(
                content="Maaf, saya tidak dapat membantu dengan informasi pribadi atau identitas pemilik akun. Jika ada pertanyaan lain yang bisa saya bantu, silakan beri tahu!",
                is_user=False
            )
    
        
        response = requests.post()
        return Message(content=response, is_user=False)

    def get_suggestions():
        return [
            "Apa yang bisa saya tanyakan?",
            "Bisa bantu saya dengan hal lain?"
        ]
    
message_service = MessageService()
