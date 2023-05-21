from pydantic import BaseModel, validator


class PostQuestionsRequest(BaseModel):
    questions_num: int

    @validator('questions_num')
    def ge0(cls, v):
        assert v >= 0
        return v
