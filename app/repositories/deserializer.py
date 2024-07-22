from typing import Dict, Any, Type, TypeVar
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class Deserializer:
    @staticmethod
    def deserialize(data: Dict[str, Any], model_class: Type[T]) -> T:
        data_copy = data.copy()
        for field_name, field in model_class.model_fields.items():
            # unpack fields such as RIDs who arrive as strings but are deserialized by using
            # their 'from_string' class method, converting into a RID type
            if field_name in data and hasattr(field.annotation, 'from_string'):
                data_copy[field_name] = field.annotation.from_string(data[field_name])

        return model_class.model_validate(data_copy)
