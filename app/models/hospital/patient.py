###############################################################################
# General Info
###############################################################################
# Description: Patient (i.e. a single individual's identifier). Each individual
# may have limitless "encounter" (clinical episodes).

###############################################################################
# Dependencies
###############################################################################

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

from app.models.general.rid import RID, RIDEntity
from app.models.general.phone_number import PhoneNumber
from app.models.general.language import Language
from app.models.general.rid_enums import RIDRootIdentifier
from app.models.general.sex import Sex


###############################################################################
# Patient
###############################################################################


class PatientRID(RID):
    entity_type: RIDEntity = Field(default=RIDEntity.PATIENT, frozen=True)
    root_identifier: RIDRootIdentifier = Field(default=RIDRootIdentifier.PATIENT_EXPERIENCE, frozen=True)


class Patient(BaseModel):
    rid: PatientRID = Field(default_factory=PatientRID.generate)

    class PatientAttributes(BaseModel):
        first_name: str
        last_name: str
        sex: Sex
        dob: date
        phone_number: PhoneNumber
        primary_language: Optional[Language]
        last_four_ssn: Optional[str]

    patient_attributes: PatientAttributes
