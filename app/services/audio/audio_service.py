import base64


class AudioService:
    @staticmethod
    def decode_twilio_audio_from_payload(payload: str) -> bytes:
        return base64.b64decode(payload)
