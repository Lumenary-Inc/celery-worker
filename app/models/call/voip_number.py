###############################################################################
# General Info
###############################################################################
# Description: Config for VoIP number


###############################################################################
# Dependencies
###############################################################################

from pydantic import BaseModel, Field

from app.models.general.rid import RID, RIDEntity
from app.models.general.rid_enums import RIDRootIdentifier
from app.models.hospital.employee import EmployeeRID
from app.models.general.phone_number import PhoneNumber

###############################################################################
# VoIP Number
###############################################################################


class VoIPNumberConfigRID(RID):
    entity_type: RIDEntity = Field(default=RIDEntity.VOIP_NUMBER, frozen=True)
    root_identifier: RIDRootIdentifier = Field(default=RIDRootIdentifier.PATIENT_EXPERIENCE, frozen=True)


class VoIPNumberConfig(BaseModel):
    rid: VoIPNumberConfigRID = Field(default_factory=VoIPNumberConfigRID.generate)
    number: PhoneNumber
    employee_owner: EmployeeRID
