import re
from typing import ClassVar
from app.models.general.rid_enums import RIDEntity, RIDRootIdentifier


class InvalidRIDFormatError(ValueError):
    pass


class InvalidRIDComponentError(ValueError):
    pass


class ResourceIdentifierService:
    SEPARATOR: ClassVar[str] = "."
    ROOT_IDENTIFIER_PATTERN: ClassVar[re.Pattern] = re.compile(r'^[a-z][a-z0-9\-]*$')
    ENTITY_PATTERN: ClassVar[re.Pattern] = re.compile(r'^[a-z][a-z0-9\-]*$')
    LOCATION_PATTERN: ClassVar[re.Pattern] = re.compile(r'^[a-zA-Z0-9\-\._]+$')
    RID_PATTERN: ClassVar[re.Pattern] = re.compile(r'^[a-z][a-z0-9\-]*\.[a-z][a-z0-9\-]*\.[a-zA-Z0-9\-\._]+$')

    @staticmethod
    def validate(rid_string: str) -> bool:
        if not rid_string or not ResourceIdentifierService.RID_PATTERN.match(rid_string):
            raise InvalidRIDFormatError(f"RID does not match the required format: {rid_string}")

        components = rid_string.split(ResourceIdentifierService.SEPARATOR)
        if len(components) != 3:
            raise InvalidRIDFormatError(f"RID must have exactly three components: {rid_string}")

        root_identifier, entity_type, location = components

        if not ResourceIdentifierService._is_valid_root_identifier(root_identifier):
            raise InvalidRIDComponentError(f"Invalid root identifier: {root_identifier}")

        if not ResourceIdentifierService._is_valid_entity_type(entity_type):
            raise InvalidRIDComponentError(f"Invalid entity type: {entity_type}")

        if not ResourceIdentifierService._is_valid_location(location):
            raise InvalidRIDComponentError(f"Invalid location: {location}")

        return True

    @staticmethod
    def _is_valid_root_identifier(root_identifier: str) -> bool:
        return root_identifier in RIDRootIdentifier.__members__.values()

    @staticmethod
    def _is_valid_entity_type(entity_type: str) -> bool:
        return entity_type in RIDEntity.__members__.values()

    @staticmethod
    def _is_valid_location(location: str) -> bool:
        return ResourceIdentifierService.LOCATION_PATTERN.match(location) is not None
