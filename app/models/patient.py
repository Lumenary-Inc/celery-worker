from pydantic import BaseModel


class Patient(BaseModel):
    id: int
    first_name: str
    last_name: str
    contact_number: str
