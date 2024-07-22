from typing import List
from pydantic import BaseModel


# stubbed for Conversation
class Transcript(BaseModel):
    id: int
    campaign_id: int
    patient_id: int
    utterances: List[str]
