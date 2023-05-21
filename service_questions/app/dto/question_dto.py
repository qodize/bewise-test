import datetime
from pydantic import BaseModel


class QuestionDto(BaseModel):
    id: int
    question: str
    answer: str
    created_at: datetime.datetime


QuestionDto.update_forward_refs()
