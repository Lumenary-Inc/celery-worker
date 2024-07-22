###############################################################################
# General Info
###############################################################################
# Description: Implementation of Resource Identifier Type (the primary way
# by which we reference our various persisted objects)
from typing import Type, TypeVar

###############################################################################
# Dependencies
###############################################################################

from pydantic import BaseModel, model_serializer
from uuid import UUID, uuid4

from app.models.general.rid_enums import RIDRootIdentifier, RIDEntity
from app.services.rid.resource_identifier_service import ResourceIdentifierService


###############################################################################
# RID
###############################################################################


T = TypeVar("T", bound="RID")


class RID(BaseModel):
    root_identifier: RIDRootIdentifier
    entity_type: RIDEntity
    location: UUID

    @classmethod
    def generate(cls: Type[T]) -> T:
        root_identifier = cls.model_fields['root_identifier'].default
        entity_type = cls.model_fields['entity_type'].default

        if root_identifier is None or entity_type is None:
            raise ValueError(f"Default values for root_identifier and entity_type must be provided in {cls.__name__}")

        return cls(
            root_identifier=root_identifier,
            entity_type=entity_type,
            location=uuid4()
        )

    @model_serializer
    def serialize_rid(self) -> str:
        # consideration should be placed here if we'd like to store the entity type & location separately
        # so that in the case of a RENAME of entity, we can quickly find all affected RIDs and swap them out without
        # downtime or large queries on the db, storing just the RID for now.
        return self.to_string()

    def to_string(self) -> str:
        components = [self.root_identifier.value, self.entity_type.value, str(self.location)]
        return ResourceIdentifierService.SEPARATOR.join(components)

    @classmethod
    def from_string(cls: Type[T], rid_string: str) -> T:
        if not ResourceIdentifierService.validate(rid_string):
            raise ValueError(f"Invalid RID format: {rid_string}")

        components = rid_string.split(ResourceIdentifierService.SEPARATOR)
        root_identifier, entity_type, location = components

        # we should be more strict here, if we attempt to deser RID to class X
        # but it belongs to class Y, we perform the conversation automatically
        # we should throw here when that happens

        return cls(
            root_identifier=RIDRootIdentifier(root_identifier),
            entity_type=RIDEntity(entity_type),
            location=UUID(location)
        )

    def __str__(self):
        return self.to_string()

    def __eq__(self, other):
        if not isinstance(other, RID):
            return False
        return self.to_string() == other.to_string()

    def __hash__(self):
        return hash(self.to_string())
