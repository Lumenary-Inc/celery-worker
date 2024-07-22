from app.database.session import get_supabase_client
from fastapi import HTTPException

from app.models.raw_conversation.utterance import Utterance, UtteranceCreate


class UtteranceRepository:
    def __init__(self):
        self.supabase = get_supabase_client()

    def add_utterance(self, utterance: UtteranceCreate) -> Utterance:
        response = self.supabase.table("utterances").insert(utterance.model_dump()).execute()
        data = response.data
        if not data:
            raise HTTPException(status_code=500, detail="Failed to create transcript")
        return Utterance(**data[0])
