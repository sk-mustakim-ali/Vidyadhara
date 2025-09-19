from fastapi import APIRouter
from controllers import quiz_controller

router = APIRouter()

@router.post("/")
async def create_quiz(payload: dict):
    return await quiz_controller.create_quiz(payload)

@router.get("/lesson/{lesson_id}")
async def quizzes_for_lesson(lesson_id: str):
    return await quiz_controller.quizzes_for_lesson(lesson_id)

@router.post("/{quiz_id}/attempt")
async def attempt_quiz(quiz_id: str, payload: dict):
    return await quiz_controller.attempt_quiz(quiz_id, payload)

@router.get("/{quiz_id}")
async def get_quiz(quiz_id: str):
    return await quiz_controller.get_quiz(quiz_id)
