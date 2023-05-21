import typing
from service_questions.app.dto.question_dto import QuestionDto
from service_questions.app.exceptions.already_exists_error import AlreadyExistsError
from service_questions.app.exceptions.bad_request_error import BadRequestError
from service_questions.app.repos.abstract.quiz_db_repo_abc import QuizDatabaseRepoABC
from service_questions.app.repos.abstract.quiz_find_repo_abc import QuizFindRepoABC
from service_questions.app.services.abstract.quiz_service_abc import QuizServiceABC


class QuizService(QuizServiceABC):
    def __init__(self, quiz_find_repo: QuizFindRepoABC, quiz_db_repo: QuizDatabaseRepoABC):
        self.quiz_find_repo = quiz_find_repo
        self.quiz_db_repo = quiz_db_repo

    async def fetch_questions(self, questions_num: int) -> typing.Optional[QuestionDto]:
        last_saved: typing.Optional[QuestionDto] = None
        while questions_num:
            try:
                questions = await self.quiz_find_repo.find(questions_num)
            except BadRequestError as e:
                raise e
            questions_num = 0

            for question in questions:
                try:
                    last_saved = await self.quiz_db_repo.insert_one(question)
                except AlreadyExistsError:
                    questions_num += 1
        return last_saved
