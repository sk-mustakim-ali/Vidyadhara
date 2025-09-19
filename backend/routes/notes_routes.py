from fastapi import APIRouter
from controllers import notes_controller

router = APIRouter()

@router.get("/lesson/{lesson_id}")
async def get_notes(lesson_id: str):
    return await notes_controller.get_notes_for_lesson(lesson_id)

@router.post("/")
async def add_note(payload: dict):
    return await notes_controller.add_note(payload)

@router.delete("/{note_id}")
async def delete_note(note_id: str):
    return await notes_controller.delete_note(note_id)
