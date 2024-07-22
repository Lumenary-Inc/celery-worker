import base64
from collections import deque
from typing import Dict, Deque
from app.models.audio.audio_chunk import IndividualAudioChunk, MergedAudioChunk
from app.repositories.audio_chunk_repository import AudioChunkRepository


class AudioWriterService:
    def __init__(self, audio_chunk_db: AudioChunkRepository, chunk_block_size: int = 10):
        self.chunk_block_size = chunk_block_size
        self.audio_chunk_db = audio_chunk_db
        self.accumulated_chunks: Dict[int, Deque[IndividualAudioChunk]] = {}

    def accumulate_then_save_chunk(self, call_id: int, audio_chunk: IndividualAudioChunk):
        if call_id not in self.accumulated_chunks:
            self.accumulated_chunks[call_id] = deque()
        self.accumulated_chunks[call_id].append(audio_chunk)

        if len(self.accumulated_chunks[call_id]) >= self.chunk_block_size:
            self.save_combined_chunk(call_id)

    def save_combined_chunk(self, call_id: int):
        chunks = self.accumulated_chunks[call_id]

        # since b64(c) + b64(c2) ... b64(cN) != b64(c + c2 ... cN)
        # perf tested: decode -> encode takes ~171 micros for 10kb
        decoded_payloads = [base64.b64decode(chunk.payload) for chunk in chunks]
        combined_payload = b''.join(decoded_payloads)
        combined_payload_base64 = base64.b64encode(combined_payload).decode('utf-8')

        chunk_sequence_start = int(chunks[0].chunk_sequence_number)
        chunk_sequence_end = int(chunks[-1].chunk_sequence_number)
        total_chunks = len(chunks)

        combined_chunk = MergedAudioChunk(
            call_id=call_id,
            chunk_sequence_start=chunk_sequence_start,
            chunk_sequence_end=chunk_sequence_end,
            total_chunks=total_chunks,
            payload=combined_payload_base64,
        )

        self.audio_chunk_db.create_audio_chunk(combined_chunk)
        self.accumulated_chunks[call_id].clear()

    def handle_disconnect(self, call_id: int):
        if call_id in self.accumulated_chunks and self.accumulated_chunks[call_id]:
            self.save_combined_chunk(call_id)
        if call_id in self.accumulated_chunks:
            del self.accumulated_chunks[call_id]
