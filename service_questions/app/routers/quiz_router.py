import typing

from fastapi import APIRouter, Body, Depends, HTTPException
from dependency_injector.wiring import Provide, inject

from service_questions.app.dto.post_questions_request import PostQuestionsRequest
from service_questions.app.dto.question_dto import QuestionDto
from service_questions.app.exceptions.bad_request_error import BadRequestError
from service_questions.app.services.abstract.quiz_service_abc import QuizServiceABC
from service_questions.app.di.containers import Container

router = APIRouter()


@router.post(
    '/questions',
    responses={200: {'model': typing.Optional[QuestionDto], 'description': 'OK'},
               400: {'description': 'Bad request'}}
)
@inject
async def post_questions(
        request: PostQuestionsRequest = Body(None, description=""),
        quiz_service: QuizServiceABC = Depends(Provide[Container.quiz_service])
) -> typing.Optional[QuestionDto]:
    try:
        return await quiz_service.fetch_questions(request.questions_num)
    except BadRequestError:
        raise HTTPException(status_code=400, detail='Bad request')
