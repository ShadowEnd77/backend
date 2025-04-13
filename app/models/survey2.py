from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Survey(Base): #Опрос
    __tablename__ = "surve2"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    questions = relationship("Question", back_populates="survey", cascade="all, delete-orphan")

class Question(Base):#Вопрос
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    survey_id = Column(Integer, ForeignKey("surve2.id"))
    
    survey = relationship("Survey", back_populates="questions")
    options = relationship("Option", back_populates="question", cascade="all, delete-orphan")

class Option(Base): # Ответ
    __tablename__ = "options"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    score = Column(Integer, nullable=False)  # Баллы за вариант ответа
    question_id = Column(Integer, ForeignKey("questions.id"))
    
    question = relationship("Question", back_populates="options")

class UserResponse(Base):# Результаты
    __tablename__ = "user_responses"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    option_id = Column(Integer, ForeignKey("options.id"))
    survey_id = Column(Integer, ForeignKey("surve2.id"))
    
    question = relationship("Question")
    option = relationship("Option")
    survey = relationship("Survey")