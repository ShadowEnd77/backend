from sqlalchemy.orm import Session
from app.models.survey2 import Survey, Question, Option, UserResponse

def get_survey(db: Session, survey_id: int):
    return db.query(Survey).filter(Survey.id == survey_id).first()

def get_active_survey(db: Session):
    return db.query(Survey).filter(Survey.is_active == True).first()

def create_survey(db: Session, survey_data):
    db_survey = Survey(
        title=survey_data.title,
        description=survey_data.description,
        is_active=survey_data.is_active
    )
    db.add(db_survey)
    db.commit()
    db.refresh(db_survey)
    
    for question_data in survey_data.questions:
        db_question = Question(
            text=question_data.text,
            question_type=question_data.question_type,
            survey_id=db_survey.id
        )
        db.add(db_question)
        db.commit()
        db.refresh(db_question)
        
        for option_data in question_data.options:
            db_option = Option(
                text=option_data.text,
                score=option_data.score,
                question_id=db_question.id
            )
            db.add(db_option)
        
    db.commit()
    db.refresh(db_survey)
    return db_survey

def save_response(db: Session, response_data):
    db_response = UserResponse(**response_data.dict())
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    return db_response

def calculate_results(db: Session, user_id: str, survey_id: int):
    responses = db.query(UserResponse).filter(
        UserResponse.user_id == user_id,
        UserResponse.survey_id == survey_id
    ).all()

    if not responses:
        return None

    # Вопросы для экранной зависимости (2-6)
    screen_questions = {2, 3, 4, 5, 6}
    # Вопросы для игровой зависимости (7-11)
    game_questions = {7, 8, 9, 10, 11}

    screen_score = 0
    game_score = 0

    for response in responses:
        option = db.query(Option).filter(Option.id == response.option_id).first()
        if response.question_id in screen_questions:
            screen_score += option.score
        elif response.question_id in game_questions:
            game_score += option.score

    # Определение уровней зависимости
    def get_dependency_level(score, dependency_type):
        if score >= 11:
            level = "высокий уровень риска"
            if dependency_type == "screen":
                desc = "Ребенок зависим от гаджета, возможны нарушения сна и успеваемости"
            else:
                desc = "Ребенок зависим от игр, возможны проблемы с учебой и общением"
        elif 6 <= score <= 10:
            level = "средний уровень риска"
            if dependency_type == "screen":
                desc = "Регулярное, но не чрезмерное использование устройств"
            else:
                desc = "Чрезмерное увлечение играми с небольшим влиянием на учебу"
        else:
            level = "низкий уровень риска"
            if dependency_type == "screen":
                desc = "Умеренное использование гаджетов без нарушений"
            else:
                desc = "Контролируемое использование игр, хороший баланс"
        
        return level, desc

    screen_level, screen_desc = get_dependency_level(screen_score, "screen")
    game_level, game_desc = get_dependency_level(game_score, "game")

    return {
        "screen_dependency_score": screen_score,
        "game_dependency_score": game_score,
        "screen_dependency_level": screen_level,
        "game_dependency_level": game_level,
        "screen_dependency_description": screen_desc,
        "game_dependency_description": game_desc
    }