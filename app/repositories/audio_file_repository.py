from typing import Optional
from io import BytesIO

from app.database.session import get_supabase_client
from app.models.audio.audio_file import AudioFile


class AudioFileRepository:
    def __init__(self):
        self.supabase = get_supabase_client()
        self.bucket_name = "audio_files"

    # we should decouple this from being WAV if we add new decoders, too lazy at the moment
    def save_audio_file_to_bucket(self, audio_buffer: BytesIO, file_path: str):
        mime_type = 'audio/wav'
        audio_bytes = audio_buffer.getvalue()
        self.supabase.storage.from_(self.bucket_name).upload(file=audio_bytes, path=file_path,
                                                             file_options={"content-type": mime_type})

    def create_audio_file(self, audio_file: AudioFile) -> AudioFile:
        wav_data = audio_file.model_dump()
        response = self.supabase.table("audio_files").insert(wav_data).execute()
        return AudioFile(**response.data[0])

    def get_audio_file_by_call_id(self, call_id: int) -> Optional[AudioFile]:
        response = self.supabase.table("audio_files").select("*").eq("call_id", call_id).execute()
        data = response.data
        if data:
            return AudioFile(**data[0])
        return None

    def get_audio_file(self, file_path: str) -> BytesIO:
        response = self.supabase.storage.from_(self.bucket_name).download(file_path)
        return BytesIO(response)

    def delete_audio_file_for_call_id(self, call_id: int) -> bool:
        wav = self.get_audio_file_by_call_id(call_id)
        if not wav:
            return False

        self.supabase.storage.from_(self.bucket_name).remove(wav.file_path)
        response = self.supabase.table("audio_files").delete().eq("call_id", call_id).execute()
        return response.status_code == 204

    def update_audio_file(self, call_id: int, updated_audio_file: AudioFile) -> AudioFile:
        response = self.supabase.table("audio_files").update(updated_audio_file.model_dump()).eq("call_id",
                                                                                                 call_id).execute()
        return AudioFile(**response.data[0])
