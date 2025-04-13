from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class OptionBase(BaseModel):
    text: str
    score: int

class OptionCreate(OptionBase):
    pass

class Option(OptionBase):
    id: int
    question_id: int

    class Config:
        from_attributes = True

class QuestionBase(BaseModel):
    text: str

class QuestionCreate(QuestionBase):
    options: List[OptionCreate] = []

class Question(QuestionBase):
    id: int
    survey_id: int
    options: List[Option] = []

    class Config:
        from_attributes = True

class SurveyBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_active: Optional[bool] = True

class SurveyCreate(SurveyBase):
    questions: List[QuestionCreate] = []

class Survey(SurveyBase):
    id: int
    created_at: datetime
    questions: List[Question] = []

    class Config:
        from_attributes = True

class ResponseBase(BaseModel):
    user_id: str
    question_id: int
    option_id: int
    survey_id: int

class ResponseCreate(ResponseBase):
    pass

class Response(ResponseBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class SurveyResult(BaseModel):
    screen_dependency_score: int
    game_dependency_score: int
    screen_dependency_level: str
    game_dependency_level: str
    screen_dependency_description: str
    game_dependency_description: str