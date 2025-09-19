from fastapi import APIRouter
from controllers import auth_controller

router = APIRouter()

@router.post('/signup')
async def signup(payload: dict):
    return await auth_controller.signup(payload)

@router.post('/login')
async def login(payload: dict):
    return await auth_controller.login(payload)
