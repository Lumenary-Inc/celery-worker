###############################################################################
# General Info
###############################################################################
# Description: Implementation of Resource Identifier Type (the primary way
# by which we reference our various persisted objects)

###############################################################################
# Dependencies
###############################################################################

from pydantic import BaseModel, field_validator, Field
from typing import Optional, List
from enum import Enum
from app.models.general.rid import RID, RIDEntity
from app.models.general.rid_enums import RIDRootIdentifier
from app.models.hospital.location import Unit

###############################################################################
# Employee
###############################################################################


class EmployeeRID(RID):
    entity_type: RIDEntity = Field(default=RIDEntity.EMPLOYEE, frozen=True)
    root_identifier: RIDRootIdentifier = Field(default=RIDRootIdentifier.PATIENT_EXPERIENCE, frozen=True)


class EmployeeRole(str, Enum):
    DOCTOR = "doctor"
    NURSE = "nurse"
    ADMINISTRATOR = "administrator"


class Employee(BaseModel):
    rid: EmployeeRID = Field(default_factory=EmployeeRID.generate)

    class EmployeeAttributes(BaseModel):
        first_name: Optional[str]
        last_name: str
        role: EmployeeRole
        credentials: List[str]
        units: List[Unit]

    employee_attributes: EmployeeAttributes
