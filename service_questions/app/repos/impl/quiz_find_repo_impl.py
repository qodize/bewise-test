import asyncio
import typing
from aiohttp import ClientSession

from service_questions.app.dto.create_question_dto import CreateQuestionDto
from service_questions.app.exceptions.bad_request_error import BadRequestError
from service_questions.app.repos.abstract.quiz_find_repo_abc import QuizFindRepoABC


class JServiceQuizFindRepo(QuizFindRepoABC):
    async def find(self, questions_num: int) -> list[CreateQuestionDto]:
        if questions_num < 0:
            raise BadRequestError()
        async with ClientSession() as session:
            async with session.get(f'https://jservice.io/api/random?count={questions_num}') as resp:
                return [CreateQuestionDto.parse_obj(question) for question in await resp.json()]
