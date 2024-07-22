###############################################################################
# General Info
###############################################################################
# Description: Encounters correspond to specific clinical episodes of the
# patient

###############################################################################
# Dependencies
###############################################################################

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

from app.models.general.rid import RID, RIDEntity
from app.models.general.rid_enums import RIDRootIdentifier
from app.models.hospital.location import UnitRID
from app.models.hospital.location import FacilityRID
from app.models.hospital.patient import PatientRID
from app.models.hospital.employee import EmployeeRID

###############################################################################
# Encounters
###############################################################################


class EncounterRID(RID):
    entity_type: RIDEntity = Field(default=RIDEntity.ENCOUNTER, frozen=True)
    root_identifier: RIDRootIdentifier = Field(default=RIDRootIdentifier.PATIENT_EXPERIENCE, frozen=True)


class Encounter(BaseModel):
    rid: EncounterRID = Field(default_factory=EncounterRID.generate)
    patient_rid: PatientRID
    start_date: date
    # They might still be in the hospital e.g. rounding
    end_date: Optional[date]
    involved_units: List[UnitRID]
    involved_facilities: List[FacilityRID]
    involved_employees: List[EmployeeRID]
