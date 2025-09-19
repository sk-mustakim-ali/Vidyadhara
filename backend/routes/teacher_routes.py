from fastapi import APIRouter, Body
from controllers import teacher_controller

router = APIRouter(tags=["Teacher"])  # ⬅️ removed prefix here

# --------------------
# Lesson Endpoints
# --------------------
@router.post("/lessons")
async def add_lesson(payload: dict = Body(...)):
    """Teacher adds a new lesson"""
    return await teacher_controller.add_content(payload)

# --------------------
# Assignment Endpoints
# --------------------
@router.post("/assignments")
async def create_assignment(payload: dict = Body(...)):
    """Teacher assigns homework (assignment)"""
    return await teacher_controller.create_homework(payload)

# --------------------
# Submission Endpoints
# --------------------
@router.get("/submissions")
async def list_submissions():
    """Teacher views all student submissions"""
    return await teacher_controller.get_submissions()
