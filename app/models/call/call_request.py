###############################################################################
# General Info
###############################################################################
# Description: Initiate a call request for an agent-led campaign


###############################################################################
# Dependencies
###############################################################################

from pydantic import BaseModel, Field
from typing import Optional

from app.models.general.rid import RID, RIDEntity
from app.models.call.campaign import CampaignRID
from app.models.general.rid_enums import RIDRootIdentifier
from app.models.hospital.encounter import EncounterRID
from app.models.agent.agent_config import AgentConfigRID
from datetime import datetime


###############################################################################
# Call Request
###############################################################################


class CallRequestRID(RID):
    entity_type: RIDEntity = Field(default=RIDEntity.CALL_REQUEST, frozen=True)
    root_identifier: RIDRootIdentifier = Field(default=RIDRootIdentifier.PATIENT_EXPERIENCE, frozen=True)

# Notice that CallRequest does not contain a status field. The status is
# easily inferrible from the Call object, which lists its CallRequest if it is
# an AgentOutbound call. Once call_time >= now, there will be a corresponding
# call object that we can use for status. If call_time < now, we know the call
# is scheduled but has not yet happened.


class CallRequest(BaseModel):
    rid: CallRequestRID = Field(default_factory=CallRequestRID.generate)
    campaign_rid: CampaignRID
    encounter_rid: EncounterRID
    call_time: datetime
    notes: Optional[str] = None

    # The agent config that we'd like to make the call. Note that this is in
    # CallRequest and *not* in Campaign. Campaign should contain attributes that
    # should largely be exposed to those making campaigns. This field is
    # generally for developer purposes, to track the specific model versions
    # making the calls (probably selected in the matching engine).
    agent_config: AgentConfigRID
