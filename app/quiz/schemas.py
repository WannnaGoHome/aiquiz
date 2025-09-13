from pydantic import BaseModel
from typing import List, Optional


class QuizBase(BaseModel):
    title: str
    description: Optional[str] = None


class QuizCreate(QuizBase):
    pass


class QuizUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class QuizRead(QuizBase):
    id: int

    class Config:
        from_attributes = True

class QuizQuestionBase(BaseModel):
    text: str


class QuizQuestionCreate(QuizQuestionBase):
    quiz_id: int


class QuizQuestionUpdate(BaseModel):
    text: Optional[str] = None


class QuizQuestionRead(QuizQuestionBase):
    id: int
    quiz_id: int

    class Config:
        from_attributes = True

class UserAnswerBase(BaseModel):
    user_id: int
    answer: str


class UserAnswerCreate(UserAnswerBase):
    question_id: int


class UserAnswerUpdate(BaseModel):
    answer: Optional[str] = None


class UserAnswerRead(UserAnswerBase):
    id: int
    question_id: int

    class Config:
        from_attributes = True