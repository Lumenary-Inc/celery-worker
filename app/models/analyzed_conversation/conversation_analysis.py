###############################################################################
# General Info
###############################################################################
# Description: Output of insight extraction engine


###############################################################################
# Dependencies
###############################################################################

from pydantic import BaseModel, Field
from typing import Optional, List, Union
from enum import Enum
from datetime import date

from app.models.general.rid import RID, RIDEntity
from app.models.general.rid_enums import RIDRootIdentifier
from app.models.hospital.location import UnitRID
from app.models.hospital.employee import EmployeeRID
from app.models.processed_conversation.turned_conversation import (
    Message,
    Interruption,
)
from app.models.agent.agentic_action import AgenticAction
from app.models.call.performance_question import PerformanceQuestion
from app.models.call.call import CallRID
from app.models.analyzed_conversation.tag import TagRID


###############################################################################
# Analysis Objects
###############################################################################


class ClusterRID(RID):
    entity_type: RIDEntity = Field(default=RIDEntity.CLUSTER, frozen=True)
    root_identifier: RIDRootIdentifier = Field(default=RIDRootIdentifier.PATIENT_EXPERIENCE, frozen=True)


class Cluster(BaseModel):
    rid: ClusterRID = Field(default_factory=ClusterRID.generate)
    performance_question: Optional[PerformanceQuestion]
    cluster_name: str


class Sentiment(str, Enum):
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    POSITIVE = "positive"


class ConversationChunk(BaseModel):
    conversation_chunk: List[Union[Message, Interruption, AgenticAction]]
    starting_idx_in_parent: int
    relevant_performance_question: PerformanceQuestion
    relevant_units: List[UnitRID]
    relevant_employees: List[EmployeeRID]
    tags_last_updated: date
    relevant_tags: List[TagRID]
    sentiment: Optional[Sentiment]
    summary: Optional[str]
    cluster_rid: Optional[ClusterRID]


class ConversationAnalysis(BaseModel):
    call_rid: CallRID
    conversation_chunks: List[ConversationChunk]
    summary: str
