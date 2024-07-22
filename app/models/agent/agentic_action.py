###############################################################################
# General Info
###############################################################################
# Description: Define mostly abstract agent transition types for specific
# agents to implement


###############################################################################
# Dependencies
###############################################################################

from pydantic import BaseModel
from typing import Optional, Union
from app.models.processed_conversation.speaker import AgentSpeaker
from abc import ABC


###############################################################################
# Agentic Transitions
###############################################################################


# Triggers a change of the agent FSM state (or hangup)
class AgenticHardTransition(BaseModel, ABC):
    pass


# Coerces the agent via thoughts and only uses transition field for labeling
# those thoughts (but not changing the FSM state)
class AgenticSoftTransition(BaseModel, ABC):
    pass


class AgenticReaction(BaseModel):
    reason: str
    thought: Optional[str]
    transition: Optional[Union[AgenticHardTransition, AgenticSoftTransition]]


class AgenticAction(BaseModel):
    speaker: AgentSpeaker
    action_data: Union[AgenticReaction]
