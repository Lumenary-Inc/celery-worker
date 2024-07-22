import wave
import base64
import audioop
from io import BytesIO
from typing import List

from app.config import logger
from app.celery_app import celery
from app.models.audio.audio_chunk import MergedAudioChunk
from app.models.audio.audio_file import AudioFileFormat, AudioFile
from app.repositories.audio_chunk_repository import AudioChunkRepository
from app.repositories.audio_file_repository import AudioFileRepository
from app.services.audio_enhance_service import enhance_and_persist_audio


def create_audio_file_from_chunks(audio_chunks: List[MergedAudioChunk]):
    if not audio_chunks:
        return None, None, None

    logger.info(f"***** Processing {len(audio_chunks)} audio chunks")
    decoded_audio_chunks = [base64.b64decode(chunk.payload) for chunk in audio_chunks]

    def mulaw_to_pcm(mu_law_bytes):
        return audioop.ulaw2lin(mu_law_bytes, sample_width)

    n_channels = 1
    framerate = 8000
    sample_width = 2

    wav_buffer = BytesIO()
    with wave.open(wav_buffer, 'wb') as wav_file:
        wav_file.setnchannels(n_channels)
        wav_file.setsampwidth(sample_width)
        wav_file.setframerate(framerate)
        [wav_file.writeframes(mulaw_to_pcm(chunk)) for chunk in decoded_audio_chunks]

    wav_buffer.seek(0)
    file_size_mb = wav_buffer.getbuffer().nbytes / (1024 * 1024)
    total_samples = sum(len(chunk) // sample_width for chunk in decoded_audio_chunks)
    duration = total_samples / framerate

    return wav_buffer, file_size_mb, duration


@celery.task
def persist_audio_file(call_id: int) -> None:
    audio_file_repository = AudioFileRepository()
    audio_chunk_repository = AudioChunkRepository()
    audio_chunks: List[MergedAudioChunk] = audio_chunk_repository.get_all_audio_chunks_for_call_id(call_id)

    logger.info(f"***** Organizing chunks into audio file for: {call_id}")
    audio_buffer, file_size_mb, duration = create_audio_file_from_chunks(audio_chunks)
    logger.info(f"***** Audio file created in memory for: {call_id}")

    if audio_buffer and file_size_mb and duration:
        file_path = f"{call_id}/{call_id}.wav"
        audio_file_create = AudioFile(
            call_id=call_id,
            file_path=file_path,
            duration=duration,
            file_size_mb=file_size_mb,
            file_format=AudioFileFormat.WAV
        )

        audio_file_repository.save_audio_file_to_bucket(audio_buffer, file_path)
        audio_file_repository.create_audio_file(audio_file_create)

        logger.info(f"***** WAV created for: {call_id}")
        logger.info(f"***** Enhancing now...")
        enhance_and_persist_audio(audio_buffer, call_id)
