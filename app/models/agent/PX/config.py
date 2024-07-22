###############################################################################
# General Info
###############################################################################
# Description: AgentConfigRID for PX-style agents


###############################################################################
# Dependencies
###############################################################################


from pydantic import Field
from app.models.general.rid import RIDEntity
from app.models.agent.agent_config import AgentConfigRID
from app.models.general.rid_enums import RIDRootIdentifier


###############################################################################
# PX Agent Config RID
###############################################################################


class PXAgentConfigRID(AgentConfigRID):
    entity_type: RIDEntity = Field(default=RIDEntity.PX_AGENT_CONFIG, frozen=True)
    root_identifier: RIDRootIdentifier = Field(default=RIDRootIdentifier.PATIENT_EXPERIENCE, frozen=True)
