###############################################################################
# General Info
###############################################################################
# Description: Implementation of Resource Identifier Type (the primary way
# by which we reference our various persisted objects)

###############################################################################
# Dependencies
###############################################################################

from pydantic import BaseModel, field_validator, Field
import re


###############################################################################
# Phone Number
###############################################################################


class PhoneNumber(BaseModel):
    number: str = Field(..., min_length=10, max_length=15)

    @field_validator("origin", mode="before", check_fields=False)
    def validate_phone_number(cls, v):
        pattern = r"^\+?1?\d{9,14}$"
        if not re.match(pattern, v):
            raise ValueError("Invalid phone number format")
        return v

    def __str__(self):
        return self.number
