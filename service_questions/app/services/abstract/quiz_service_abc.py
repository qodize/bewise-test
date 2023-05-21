import typing
import abc

from service_questions.app.dto.question_dto import QuestionDto


class QuizServiceABC(abc.ABC):
    @abc.abstractmethod
    async def fetch_questions(self, questions_num: int) -> typing.Optional[QuestionDto]:
        ...
