from fastapi import APIRouter
from controllers import subject_controller

router = APIRouter()

@router.get("/")
async def list_subjects():
    return await subject_controller.list_subjects()

@router.get("/{subject_id}/lessons")
async def lessons_by_subject(subject_id: str):
    return await subject_controller.lessons_by_subject(subject_id)

@router.post("/")
async def create_subject(payload: dict):
    return await subject_controller.create_subject(payload)
