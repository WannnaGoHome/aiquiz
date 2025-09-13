from fastapi import APIRouter, Depends
from app.quiz import schemas
from app.quiz.services import QuizService
from app.users.models import User
from app.common.common import CurrentUser

router = APIRouter(prefix="/quiz", tags=["quiz"])


# ---- Quiz ----
@router.get("/{quiz_id}", response_model=schemas.QuizRead)
async def get_quiz(quiz_id: int, service: QuizService = Depends()):
    return await service.get_quiz(quiz_id)


@router.post("/", response_model=schemas.QuizRead)
async def create_quiz(data: schemas.QuizCreate, service: QuizService = Depends()):
    return await service.create_quiz(data)


@router.get("/", response_model=list[schemas.QuizRead])
async def list_quizzes(service: QuizService = Depends()):
    return await service.list_quizzes()


# ---- Questions ----
@router.get("/{quiz_id}/questions", response_model=list[schemas.QuizQuestionRead])
async def list_questions(quiz_id: int, service: QuizService = Depends()):
    return await service.list_questions(quiz_id)


@router.post("/questions", response_model=schemas.QuizQuestionRead)
async def create_question(data: schemas.QuizQuestionCreate, service: QuizService = Depends()):
    return await service.create_question(data)


# ---- Answers ----
@router.post("/answers", response_model=schemas.UserAnswerRead)
async def create_user_answer(data: schemas.UserAnswerCreate, service: QuizService = Depends()):
    return await service.create_user_answer(data)


@router.get("/questions/{question_id}/answers", response_model=list[schemas.UserAnswerRead])
async def list_user_answers(question_id: int, service: QuizService = Depends()):
    return await service.list_user_answers(question_id)


# ---- Current Question ----
@router.get("/{event_id}/current_question")
async def get_current_question(event_id: int, service: QuizService = Depends()):
    return await service.get_current_question(event_id)
