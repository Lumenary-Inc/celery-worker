###############################################################################
# General Info
###############################################################################
# Description: Config for rounding number


###############################################################################
# Dependencies
###############################################################################

from pydantic import BaseModel, Field

from app.models.general.rid import RID, RIDEntity
from app.models.general.rid_enums import RIDRootIdentifier
from app.models.hospital.employee import EmployeeRID
from app.models.general.phone_number import PhoneNumber

###############################################################################
# Rounding Number
###############################################################################


class RoundingNumberConfigRID(RID):
    entity_type: RIDEntity = Field(default=RIDEntity.ROUNDING_NUMBER, frozen=True)
    root_identifier: RIDRootIdentifier = Field(default=RIDRootIdentifier.PATIENT_EXPERIENCE, frozen=True)


class RoundingNumberConfig(BaseModel):
    rid: RoundingNumberConfigRID = Field(default_factory=RoundingNumberConfigRID.generate)
    number: PhoneNumber
    employee_owner: EmployeeRID
