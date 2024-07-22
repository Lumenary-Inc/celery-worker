from enum import Enum


class RIDRootIdentifier(str, Enum):
    PATIENT_EXPERIENCE = "px"


class RIDEntity(str, Enum):
    PATIENT = "patient"
    EMPLOYEE = "employee"
    UNIT = "unit"
    FACILITY = "facility"
    ENCOUNTER = "encounter"
    CAMPAIGN = "campaign"
    CALL_REQUEST = "call-request"
    CALL = "call"
    VOIP_NUMBER = "voip-number"
    ROUNDING_NUMBER = "rounding-number"
    PX_AGENT_CONFIG = "px-agent-config"
    CLUSTER = "cluster"
    TAG = "tag"
