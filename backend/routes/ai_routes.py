from fastapi import APIRouter
from controllers import ai_controller

router = APIRouter()

@router.post("/chat")
async def ai_chat(payload: dict):
    return await ai_controller.ai_chat(payload)

@router.post("/teacher-feedback")
async def teacher_feedback(payload: dict):
    return await ai_controller.teacher_feedback(payload)

@router.get("/progress/{student_id}")
async def progress_report(student_id: str):
    return await ai_controller.progress_report(student_id)

@router.get("/recommendation/{student_id}")
async def ai_recommendation(student_id: str):
    return await ai_controller.ai_recommendation(student_id)

@router.post("/assign-task")
async def assign_task(payload: dict):
    return await ai_controller.assign_task(payload)
