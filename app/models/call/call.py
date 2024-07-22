###############################################################################
# General Info
###############################################################################
# Description: Create an identifier for all calls to link audio and all
# generated call artifacts (raw conversation, turned conversation, etc.)

###############################################################################
# Dependencies
###############################################################################

from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional

from app.models.general.rid import RID, RIDEntity
from app.models.general.rid_enums import RIDRootIdentifier
from app.models.hospital.encounter import EncounterRID
from app.models.call.call_request import CallRequestRID
from app.models.call.rounding_number import RoundingNumberConfigRID
from app.models.call.voip_number import VoIPNumberConfigRID
from app.models.general.phone_number import PhoneNumber
from abc import ABC


from datetime import datetime


###############################################################################
# Call Metadata (All types of calls have a call agent created for them, but
# we need some way of distinguishing between the various call types and holding
# all the necessary attributes for each)
###############################################################################


class CallMetadata(BaseModel, ABC):
    relevant_encounter: EncounterRID


class CallMetadataVoIP(CallMetadata):
    relevant_encounter: Optional[EncounterRID]
    voip_number_config_rid: VoIPNumberConfigRID


class CallMetadataRounding(CallMetadata):
    relevant_encounter: Optional[EncounterRID]
    rounding_number_config_rid: RoundingNumberConfigRID


class CallMetadataAgentOutbound(CallMetadata):
    call_request_rid: CallRequestRID  # Includes agent and campaign info
    relevant_encounter: EncounterRID


###############################################################################
# Call
###############################################################################


class CallStatus(str, Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class CallRID(RID):
    entity_type: RIDEntity = Field(default=RIDEntity.CALL, frozen=True)
    root_identifier: RIDRootIdentifier = Field(default=RIDRootIdentifier.PATIENT_EXPERIENCE, frozen=True)


class Call(BaseModel):
    rid: CallRID = Field(default_factory=CallRID.generate)
    called_number: PhoneNumber
    call_status: CallStatus
    calling_number: PhoneNumber
    call_metadata: CallMetadata
    call_time_start: datetime
    call_duration: float
