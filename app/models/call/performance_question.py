from pydantic import BaseModel


class PerformanceQuestion(BaseModel):
    question: str
