from app.database.session import get_supabase_client
from app.models.transcript import Transcript
from typing import List
from fastapi import HTTPException


class TranscriptRepository:
    def __init__(self):
        self.supabase = get_supabase_client()

    def get_transcript_by_id(self, transcript_id: int) -> Transcript:
        response = self.supabase.table("transcripts").select("*").eq("id", transcript_id).execute()
        data = response.data
        if not data:
            raise HTTPException(status_code=404, detail="Transcript not found")
        return Transcript(**data[0])

    def create_transcript(self, transcript: Transcript) -> Transcript:
        response = self.supabase.table("transcripts").insert(transcript.dict(exclude_unset=True)).execute()
        data = response.data
        if not data:
            raise HTTPException(status_code=500, detail="Failed to create transcript")
        return Transcript(**data[0])

    def get_transcripts_by_campaign(self, campaign_id: int) -> List[Transcript]:
        response = self.supabase.table("transcripts").select("*").eq("campaign_id", campaign_id).execute()
        data = response.data
        if not data:
            raise HTTPException(status_code=404, detail="Transcripts not found")
        return [Transcript(**transcript) for transcript in data]
