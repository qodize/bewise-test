import abc


class QuizServiceABC(abc.ABC):
    @abc.abstractmethod
    async def get_questions(self, questions_num: int):
        ...
