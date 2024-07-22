###############################################################################
# General Info
###############################################################################
# Description: Persistence of audio files


###############################################################################
# Dependencies
###############################################################################

from pydantic import BaseModel
from app.models.call.call import CallRID
from typing import Optional
from enum import Enum
from pathlib import Path


###############################################################################
# AudioFile
###############################################################################


class AudioFileFormat(str, Enum):
    WAV = "wav"
    # MP3 = "mp3"
    # AAC = "aac"
    # FLAC = "flac"
    # OGG = "ogg"
    # M4A = "m4a"


class AudioFile(BaseModel):
    call_rid: CallRID
    duration: float
    file_size_mb: float
    file_format: AudioFileFormat
    file_path: Path
    enhanced_file_path: Optional[str] = ""
