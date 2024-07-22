from typing import Dict, Type

from app.models.agent.PX.config import PXAgentConfigRID
from app.models.analyzed_conversation.conversation_analysis import ClusterRID
from app.models.analyzed_conversation.tag import TagRID
from app.models.call.call import CallRID
from app.models.call.call_request import CallRequestRID
from app.models.call.campaign import CampaignRID
from app.models.call.rounding_number import RoundingNumberConfigRID
from app.models.call.voip_number import VoIPNumberConfigRID
from app.models.general.rid import RIDEntity, RID
from app.models.hospital.employee import EmployeeRID
from app.models.hospital.encounter import EncounterRID
from app.models.hospital.location import FacilityRID, UnitRID
from app.models.hospital.patient import PatientRID

RID_TYPE_MAPPING: Dict[RIDEntity, Type[RID]] = {
    RIDEntity.PATIENT: PatientRID,
    RIDEntity.EMPLOYEE: EmployeeRID,
    RIDEntity.UNIT: UnitRID,
    RIDEntity.FACILITY: FacilityRID,
    RIDEntity.ENCOUNTER: EncounterRID,
    RIDEntity.CAMPAIGN: CampaignRID,
    RIDEntity.CALL_REQUEST: CallRequestRID,
    RIDEntity.CALL: CallRID,
    RIDEntity.VOIP_NUMBER: VoIPNumberConfigRID,
    RIDEntity.ROUNDING_NUMBER: RoundingNumberConfigRID,
    RIDEntity.PX_AGENT_CONFIG: PXAgentConfigRID,
    RIDEntity.CLUSTER: ClusterRID,
    RIDEntity.TAG: TagRID,
}
