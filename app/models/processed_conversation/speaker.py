###############################################################################
# General Info
###############################################################################
# Description: maintain speaker types for tagging who said which message

###############################################################################
# Dependencies
###############################################################################

from pydantic import BaseModel, Field
from typing import Optional
from abc import ABC

from app.models.general.rid import RID
from app.models.agent.agent_config import AgentConfigRID
from app.models.agent.PX.config import PXAgentConfigRID
from app.models.hospital.employee import EmployeeRID
from app.models.hospital.patient import PatientRID

###############################################################################
# Abstract Speaker
###############################################################################


class Speaker(BaseModel, ABC):
    rid: Optional[RID]


###############################################################################
# Agent Speakers
###############################################################################


class AgentSpeaker(BaseModel, ABC):
    rid: AgentConfigRID


class PXAgentSpeaker(BaseModel):
    rid: PXAgentConfigRID = Field(default_factory=PXAgentConfigRID.generate)


###############################################################################
# Human Speakers
###############################################################################


class HumanSpeaker(BaseModel, ABC):
    pass


class PatientSpeaker(HumanSpeaker):
    rid: PatientRID


class EmployeeSpeaker(HumanSpeaker):
    rid: EmployeeRID


class UnknownHumanSpeaker(HumanSpeaker):
    rid: None
