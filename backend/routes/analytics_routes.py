from fastapi import APIRouter
from controllers import analytics_controller

router = APIRouter()

@router.get("/student/{student_id}")
async def student_report(student_id: int):
    return await analytics_controller.get_student_report(student_id)

@router.get("/class/{teacher_id}")
async def class_report(teacher_id: int):
    return await analytics_controller.get_class_report(teacher_id)
