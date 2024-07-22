###############################################################################
# General Info
###############################################################################
# Description: Storage of PX Agent internal state (because why not)

###############################################################################
# Dependencies
###############################################################################

from pydantic import BaseModel
from typing import Optional, List, Union, Dict
from enum import Enum
from datetime import date

from app.models.call.performance_question import PerformanceQuestion
from app.models.call.campaign import VerificationRequests
from app.models.hospital.patient import PatientRID
from app.models.processed_conversation.turned_conversation import TurnedConversation

###############################################################################
# PX Agent FSM States and Agentic Actions
###############################################################################


class PXAgentState(str, Enum):
    VERIFICATION = "verification"
    CONDOLENCES = "condolences"
    Q_AND_A = "q_and_a"


###############################################################################
# PX Agent Internal State
###############################################################################


class VerificationStatus(BaseModel):
    value_to_confirm: Union[str, date, List[str]]
    n_fails: int
    confirmed: bool


class QAndAStatus(BaseModel):
    question: PerformanceQuestion
    started: bool
    finished: bool


class PXBrainState(BaseModel):
    greeting_thought: str
    fsm_state: PXAgentState
    patient: PatientRID
    questions: List[PerformanceQuestion]
    conversation: TurnedConversation
    hang_up_triggered: bool
    verification_requests: VerificationRequests
    verification_dict: Dict[str, VerificationStatus]
    current_question: Optional[PerformanceQuestion]
    q_and_a_state: List[QAndAStatus]
    current_n_empathy_nudges: int
