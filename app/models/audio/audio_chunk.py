###############################################################################
# General Info
###############################################################################
# Description: Persistence of audio chunks, which are used to construct audio
# files


###############################################################################
# Dependencies
###############################################################################

from pydantic import BaseModel
from app.models.call.call import CallRID


###############################################################################
# Audio Chunks
###############################################################################
from abc import ABC


class IndividualAudioChunk(BaseModel):
    call_rid: CallRID
    chunk_sequence_number: int
    payload: str


class MergedAudioChunk(BaseModel, ABC):
    call_rid: CallRID
    chunk_sequence_start: int
    chunk_sequence_end: int
    total_chunks: int
    payload: str
