###############################################################################
# General Info
###############################################################################
# Description: Tags for natural language-initiated linking of conversations


###############################################################################
# Dependencies
###############################################################################

from pydantic import BaseModel, Field
from app.models.general.rid import RID, RIDEntity
from app.models.general.rid_enums import RIDRootIdentifier


###############################################################################
# Tag
###############################################################################


class TagRID(RID):
    entity_type: RIDEntity = Field(default=RIDEntity.TAG, frozen=True)
    root_identifier: RIDRootIdentifier = Field(default=RIDRootIdentifier.PATIENT_EXPERIENCE, frozen=True)


class Tag(BaseModel):
    rid: TagRID = Field(default_factory=TagRID.generate)
    tag_name: str
