###############################################################################
# General Info
###############################################################################
# Description: Types corresponding to physical locations in the hospital
# e.g. Facilities and Units

###############################################################################
# Dependencies
###############################################################################

from pydantic import BaseModel, field_validator, Field
from app.models.general.rid import RID, RIDEntity
from app.models.general.rid_enums import RIDRootIdentifier


###############################################################################
# Facility
###############################################################################
class FacilityRID(RID):
    entity_type: RIDEntity = Field(default=RIDEntity.FACILITY, frozen=True)
    root_identifier: RIDRootIdentifier = Field(default=RIDRootIdentifier.PATIENT_EXPERIENCE, frozen=True)


class Facility(BaseModel):
    rid: FacilityRID = Field(default_factory=FacilityRID.generate)
    facility_name: str


###############################################################################
# Unit
###############################################################################


class UnitRID(RID):
    entity_type: RIDEntity = Field(default=RIDEntity.UNIT, frozen=True)
    root_identifier: RIDRootIdentifier = Field(default=RIDRootIdentifier.PATIENT_EXPERIENCE, frozen=True)


class Unit(BaseModel):
    rid: UnitRID = Field(default_factory=UnitRID.generate)
    unit_name: str
    facility: Facility
