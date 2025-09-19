from fastapi import APIRouter
from controllers import challenge_controller

router = APIRouter()

@router.post("/")
async def create_challenge(payload: dict):
    return await challenge_controller.create_challenge(payload)

@router.get("/")
async def list_challenges():
    return await challenge_controller.list_challenges()

@router.post("/join")
async def join_challenge(payload: dict):
    return await challenge_controller.join_challenge(payload)

@router.post("/complete")
async def complete_challenge(payload: dict):
    return await challenge_controller.complete_challenge(payload)
