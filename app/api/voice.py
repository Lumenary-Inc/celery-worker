from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.models.external.twilio import TwilioEvent, TwilioEventType
from app.models.raw_conversation.utterance import UtteranceCreate
from app.repositories.audio_chunk_repository import AudioChunkRepository
from app.models.audio.audio_chunk import IndividualAudioChunk
from app.repositories.utterances_repository import UtteranceRepository
from app.services.audio.audio_service import AudioService
from app.services.audio.audio_writer_service import AudioWriterService
from app.services.audio.deepgram.deepgram_service import DeepgramService
from app.services.jobs.pipeline.audio.audio_jobs import persist_audio_file

router = APIRouter()
utterance_repository = UtteranceRepository()
audio_service = AudioWriterService(AudioChunkRepository(), chunk_block_size=25)
deepgram_service = DeepgramService()


@router.websocket("/ws/{call_id}/stream")
async def call_stream(ws: WebSocket, call_id: str):
    await ws.accept()

    call_id = int(call_id)
    print("Setting connection...")
    deepgram_service.start_connection(call_id)
    deepgram_service.on_utterance(call_id, lambda utterance, confidence, words, sequence: utterance_repository.add_utterance(
        UtteranceCreate(
            call_id=call_id,
            utterance=utterance,
            confidence=confidence,
            words=words,
            sequence=sequence
        )
    ))

    try:
        while True:
            data = await ws.receive_json()
            event = TwilioEvent(**data)

            if event.event == TwilioEventType.MEDIA:
                audio_chunk = IndividualAudioChunk(
                    call_id=call_id,
                    chunk_sequence_number=int(event.sequenceNumber),
                    timestamp=event.media.timestamp,
                    payload=event.media.payload,
                )

                audio_bytes = AudioService.decode_twilio_audio_from_payload(event.media.payload)
                deepgram_service.send_audio_bytes(call_id, audio_bytes)
                audio_service.accumulate_then_save_chunk(call_id, audio_chunk)
            elif event.event == TwilioEventType.STOP:
                audio_service.handle_disconnect(call_id)
                break

        await ws.send_text("Done")

    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        audio_service.handle_disconnect(call_id)
        deepgram_service.finish_connection(call_id)

    persist_audio_file.apply_async(args=[call_id], queue='lumenary_pipeline_queue')
