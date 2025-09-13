from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.quiz.models import Quiz, QuizQuestion, UserAnswer
from app.quiz.schemas import QuizCreate, QuizUpdate, QuizQuestionCreate, QuizQuestionUpdate, UserAnswerCreate, UserAnswerUpdate


# ---------- Quiz ----------
async def create_quiz(session: AsyncSession, data: QuizCreate) -> Quiz:
    quiz = Quiz(**data.dict())
    session.add(quiz)
    await session.commit()
    await session.refresh(quiz)
    return quiz


async def get_quiz(session: AsyncSession, quiz_id: int) -> Quiz:
    result = await session.execute(select(Quiz).where(Quiz.id == quiz_id))
    quiz = result.scalar_one_or_none()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz


async def list_quizzes(session: AsyncSession) -> list[Quiz]:
    result = await session.execute(select(Quiz))
    return result.scalars().all()


async def update_quiz(session: AsyncSession, quiz_id: int, data: QuizUpdate) -> Quiz:
    quiz = await get_quiz(session, quiz_id)
    for field, value in data.dict(exclude_unset=True).items():
        setattr(quiz, field, value)
    await session.commit()
    await session.refresh(quiz)
    return quiz


async def delete_quiz(session: AsyncSession, quiz_id: int) -> None:
    quiz = await get_quiz(session, quiz_id)
    await session.delete(quiz)
    await session.commit()


# ---------- QuizQuestion ----------
async def create_question(session: AsyncSession, data: QuizQuestionCreate) -> QuizQuestion:
    question = QuizQuestion(**data.dict())
    session.add(question)
    await session.commit()
    await session.refresh(question)
    return question


async def get_question(session: AsyncSession, question_id: int) -> QuizQuestion:
    result = await session.execute(select(QuizQuestion).where(QuizQuestion.id == question_id))
    question = result.scalar_one_or_none()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


async def list_questions(session: AsyncSession, quiz_id: int) -> list[QuizQuestion]:
    result = await session.execute(select(QuizQuestion).where(QuizQuestion.quiz_id == quiz_id))
    return result.scalars().all()


async def update_question(session: AsyncSession, question_id: int, data: QuizQuestionUpdate) -> QuizQuestion:
    question = await get_question(session, question_id)
    for field, value in data.dict(exclude_unset=True).items():
        setattr(question, field, value)
    await session.commit()
    await session.refresh(question)
    return question


async def delete_question(session: AsyncSession, question_id: int) -> None:
    question = await get_question(session, question_id)
    await session.delete(question)
    await session.commit()

# ---------- UserAnswer ----------

async def create_user_answer(session: AsyncSession, data: UserAnswerCreate) -> UserAnswer:
    answer = UserAnswer(**data.dict())
    session.add(answer)
    await session.commit()
    await session.refresh(answer)
    return answer

async def get_user_answer(session: AsyncSession, answer_id: int) -> UserAnswer:
    result = await session.execute(select(UserAnswer).where(UserAnswer.id == answer_id))
    answer = result.scalar_one_or_none()
    if not answer:
        raise HTTPException(status_code=404, detail="UserAnswer not found")
    return answer


async def list_user_answers(session: AsyncSession, question_id: int) -> list[UserAnswer]:
    result = await session.execute(select(UserAnswer).where(UserAnswer.question_id == question_id))
    return result.scalars().all()


async def update_user_answer(session: AsyncSession, answer_id: int, data: UserAnswerUpdate) -> UserAnswer:
    answer = await get_user_answer(session, answer_id)
    for field, value in data.dict(exclude_unset=True).items():
        setattr(answer, field, value)
    await session.commit()
    await session.refresh(answer)
    return answer


async def delete_user_answer(session: AsyncSession, answer_id: int) -> None:
    answer = await get_user_answer(session, answer_id)
    await session.delete(answer)
    await session.commit()