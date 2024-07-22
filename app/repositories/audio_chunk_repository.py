from typing import List, Optional

from app.database.session import get_supabase_client
from app.models.audio.audio_chunk import MergedAudioChunk


class AudioChunkRepository:
    def __init__(self):
        self.supabase = get_supabase_client()

    def create_audio_chunk(self, audio_chunk: MergedAudioChunk) -> MergedAudioChunk:
        response = self.supabase.table("audio_chunks").insert(audio_chunk.model_dump()).execute()
        return MergedAudioChunk(**response.data[0])

    def get_audio_chunk_by_id(self, chunk_id: int) -> Optional[MergedAudioChunk]:
        response = self.supabase.table("audio_chunks").select("*").eq("id", chunk_id).execute()
        data = response.data
        if data:
            return MergedAudioChunk(**data[0])
        return None

    def get_all_audio_chunks_for_call_id(self, call_id: int) -> List[MergedAudioChunk]:
        response = (self.supabase.table("audio_chunks").select("*")
                    .eq("call_id", call_id).order("chunk_sequence_start").execute())

        return [MergedAudioChunk(**item) for item in response.data]

    def update_audio_chunk(self, chunk_id: int, audio_chunk: MergedAudioChunk) -> Optional[MergedAudioChunk]:
        response = self.supabase.table("audio_chunks").update(audio_chunk.model_dump()).eq("id", chunk_id).execute()
        data = response.data
        if data:
            return MergedAudioChunk(**data[0])
        return None

    def delete_audio_chunk(self, chunk_id: int) -> bool:
        response = self.supabase.table("audio_chunks").delete().eq("id", chunk_id).execute()
        return response.status_code == 204
