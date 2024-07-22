from pydantic import BaseModel
from typing import Optional, Dict, Any
from enum import Enum


class TwilioEventType(str, Enum):
    CONNECTED = "connected"
    START = "start"
    MEDIA = "media"
    STOP = "stop"


class TwilioTrackType(str, Enum):
    INBOUND = "inbound"


class TwilioMediaContent(BaseModel):
    track: TwilioTrackType
    chunk: str
    timestamp: str
    payload: str


class TwilioEvent(BaseModel):
    event: TwilioEventType
    streamSid: Optional[str] = None
    sequenceNumber: Optional[str] = None
    protocol: Optional[str] = None
    version: Optional[str] = None
    start: Optional[Dict[str, Any]] = None
    media: Optional[TwilioMediaContent] = None
