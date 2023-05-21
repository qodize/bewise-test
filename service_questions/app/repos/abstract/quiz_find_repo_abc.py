import abc

from service_questions.app.dto.create_question_dto import CreateQuestionDto


class QuizFindRepoABC(abc.ABC):
    @abc.abstractmethod
    async def find(self, questions_num: int) -> list[CreateQuestionDto]:
        ...
