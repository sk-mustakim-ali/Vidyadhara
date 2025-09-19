from fastapi import APIRouter
from controllers import gamification_controller

router = APIRouter()

@router.get("/leaderboard")
async def get_leaderboard():
    return await gamification_controller.get_leaderboard()

@router.get("/rewards/{student_id}")
async def get_rewards(student_id: int):
    return await gamification_controller.get_rewards(student_id)

@router.post("/rewards/{student_id}")
async def add_reward(student_id: int, payload: dict):
    return await gamification_controller.add_reward(student_id, payload)
