from collections import defaultdict
from typing import Dict, List

from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions

from app.config import settings
from app.models.raw_conversation.utterance import Word


class DeepgramService:
    def __init__(self):
        self.deepgram = DeepgramClient(settings.DEEPGRAM_API_KEY)
        self.connections: Dict[int, object] = {}
        self.sequences: Dict[int, int] = defaultdict(lambda: 0)

    def on_utterance(self, call_id, callback):
        def on_message(_, result, **kwargs):
            print(result.channel)
            utterance = result.channel.alternatives[0].transcript
            raw_words = result.channel.alternatives[0].words
            confidence = float(result.channel.alternatives[0].confidence)

            words: List[Word] = [
                Word(
                    word=w.word,
                    start=w.start,
                    end=w.end,
                    speaker=w.speaker,
                    confidence=w.confidence
                ) for w in raw_words
            ]

            if len(utterance) > 0:
                self.sequences[call_id] += 1
                callback(utterance, confidence, words, self.sequences[call_id])

        self.connections[call_id].on(LiveTranscriptionEvents.Transcript, on_message)

    def start_connection(self, call_id: int):
        options = LiveOptions(
            encoding="mulaw",
            sample_rate=8000,
            channels=1,
            model="nova-2-phonecall",
            language="en-US",
            smart_format=False,
            diarize=True
        )

        self.connections[call_id] = self.deepgram.listen.live.v("1")
        self.connections[call_id].start(options)

    def send_audio_bytes(self, call_id: int, audio_bytes: bytes):
        self.connections[call_id].send(audio_bytes)

    def finish_connection(self, call_id: int):
        if self.connections[call_id]:
            self.connections[call_id].finish()
