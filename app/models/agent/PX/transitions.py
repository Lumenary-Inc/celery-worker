###############################################################################
# General Info
###############################################################################
# Description: Specific transitions that the PX agent can implement

###############################################################################
# Dependencies
###############################################################################

from typing import Optional
from enum import Enum

from app.models.agent.agentic_action import AgenticHardTransition, AgenticSoftTransition
from app.models.agent.PX.internal_state import PXAgentState
from app.models.call.performance_question import PerformanceQuestion

###############################################################################
# Transitions
###############################################################################


class HangUpReason(str, Enum):
    BUSY = "busy"
    CALL_BACK = "call_back"
    AGGRESSION = "aggression"
    REFUSAL_TO_VERIFY = "refusal_to_verify"
    FAILURE_TO_VERIFY = "failure_to_verify"
    REQUEST_FOR_HUMAN = "request_for_human"
    REFUSAL_TO_PUT_PATIENT_ON = "refusal_to_put_patient_on"
    STALLING = "stalling"
    MEDICAL_ADVICE = "medical_advice"
    NATURAL_CAUSES = "natural_causes"


class AgenticHangUpTransition(AgenticHardTransition):
    reason: Optional[HangUpReason]


class AgenticChangeStateTransition(AgenticHardTransition):
    new_state: PXAgentState


class AgenticEmpathyNudge(AgenticSoftTransition):
    pass


class AgenticInitiateQuestionTransition(AgenticSoftTransition):
    question: PerformanceQuestion


class AgenticConcludeQuestionAndInitiateNewTransition(AgenticSoftTransition):
    question: PerformanceQuestion


class AgenticMiscellaneousQuestionTransition(AgenticSoftTransition):
    close_current_question: bool


class AgenticResumeQuestionTransition(AgenticSoftTransition):
    question: PerformanceQuestion
