from fastapi import APIRouter
from controllers import sync_controller

router = APIRouter()

@router.post("/upload")
async def upload_offline_data(payload: dict):
    return await sync_controller.upload_offline_data(payload)

@router.get("/download/{student_id}")
async def download_data(student_id: int):
    return await sync_controller.download_data(student_id)
