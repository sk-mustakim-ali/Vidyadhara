from fastapi import APIRouter
from controllers import student_controller

router = APIRouter()

@router.get("/content")
async def get_content():
    return await student_controller.get_content()

@router.post("/progress")
async def save_progress(payload: dict):
    return await student_controller.save_progress(payload)

@router.post("/homework/{assignment_id}")
async def submit_homework(assignment_id: int, payload: dict):
    return await student_controller.submit_homework(assignment_id, payload)
