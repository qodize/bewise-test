import abc

from service_questions.app.dto.create_question_dto import CreateQuestionDto
from service_questions.app.dto.question_dto import QuestionDto


class QuizDatabaseRepoABC(abc.ABC):
    @abc.abstractmethod
    async def insert_one(self, create_question: CreateQuestionDto) -> None:
        ...

    @abc.abstractmethod
    async def get_one(self, question_id: int) -> QuestionDto:
        ...

    @abc.abstractmethod
    async def get_many(self) -> list[QuestionDto]:
        ...
