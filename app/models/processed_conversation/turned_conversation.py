###############################################################################
# General Info
###############################################################################
# Description: Output of insight extraction engine


###############################################################################
# Dependencies
###############################################################################

from pydantic import BaseModel
from typing import Optional, List, Union
from datetime import datetime

from app.models.processed_conversation.speaker import Speaker
from app.models.call.call import CallRID
from app.models.agent.agentic_action import AgenticAction


###############################################################################
# Call Output (Whether PX Agent, Rounding, etc.)
###############################################################################


class Message(BaseModel):
    speaker: Speaker
    message: str
    start: datetime
    duration: float


class Interruption(BaseModel):
    time: datetime
    speaker: Optional[Speaker]


class TurnedConversation(BaseModel):
    call_rid: CallRID
    conversation: List[Union[Message, Interruption, AgenticAction]]
    start: datetime
    duration: float
