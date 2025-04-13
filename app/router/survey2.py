from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.logger import get_logger

from app.database import get_db
from app.schemas.survey2 import (
    Survey, SurveyCreate, SurveyResult,
    Response, ResponseCreate
)
from app.crud.survey2 import (
    get_survey, get_active_survey,
    create_survey, save_response,
    calculate_results
)

router = APIRouter(prefix="/surveys", tags=["Surveys"])
logger = get_logger()

@router.get("/active", response_model=Survey)
def get_active_survey_endpoint(db: Session = Depends(get_db)):
    survey = get_active_survey(db)
    if not survey:
        raise HTTPException(status_code=404, detail="No active survey found")
    return survey

@router.post("/responses", response_model=Response)
def create_response(
    response: ResponseCreate,
    db: Session = Depends(get_db)
):
    return save_response(db, response)

@router.get("/results/{user_id}", response_model=SurveyResult)
def get_survey_results(
    user_id: str,
    db: Session = Depends(get_db)
):
    survey = get_active_survey(db)
    if not survey:
        raise HTTPException(status_code=404, detail="No active survey found")
    
    results = calculate_results(db, user_id=user_id, survey_id=survey.id)
    if not results:
        raise HTTPException(status_code=404, detail="Responses not found")
    return results