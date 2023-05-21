import datetime
from pydantic import BaseModel


class CreateQuestionDto(BaseModel):
    id: int
    question: str
    answer: str
    created_at: datetime.datetime


CreateQuestionDto.update_forward_refs()
