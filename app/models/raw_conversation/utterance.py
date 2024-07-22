###############################################################################
# General Info
###############################################################################
# Description: Storage of artifacts used to create turned conversations

###############################################################################
# Dependencies
###############################################################################

from pydantic import BaseModel, Field
from typing import List

from app.models.call.call import CallRID


###############################################################################
# Raw conversation artifacts (between AudioFile and TurnedConversation)
###############################################################################


class Word(BaseModel):
    word: str
    start: float
    end: float
    confidence: float
    speaker: int


class Utterance(BaseModel):
    utterance: str
    sequence: int
    words: List[Word] = Field(default_factory=list)
    confidence: float

    class Config:
        json_encoders = {List[Word]: lambda v: [word.dict() for word in v]}


class UtteranceCreate(Utterance):
    call_rid: CallRID
