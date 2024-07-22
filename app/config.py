import os
import logging
from typing import List
from fastapi import WebSocket
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()


class Settings:
    SUPABASE_URL: str = os.getenv("SUPABASE_URL")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY")
    TW_ACCOUNT_SID: str = os.getenv("TW_ACCOUNT_SID")
    TW_AUTH_TOKEN: str = os.getenv("TW_AUTH_TOKEN")
    TW_API_KEY: str = os.getenv("TW_API_KEY")
    TW_API_SECRET: str = os.getenv("TW_API_SECRET")
    TW_TWIML_APP_SID: str = os.getenv("TW_TWIML_APP_SID")
    TW_NUMBER: str = os.getenv("TW_NUMBER")
    NGROK_URL: str = os.getenv("NGROK_URL")
    DOLBY_AUDIO_KEY: str = os.getenv("DOLBY_AUDIO_KEY")
    DOLBY_AUDIO_SECRET: str = os.getenv("DOLBY_AUDIO_SECRET")
    DEEPGRAM_API_KEY: str = os.getenv("DEEPGRAM_API_KEY")
    RABBIT_MQ_USERNAME: str = os.getenv("RABBITMQ_DEFAULT_USER")
    RABBIT_MQ_PASSWORD: str = os.getenv("RABBITMQ_DEFAULT_PASS")


settings = Settings()


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()
