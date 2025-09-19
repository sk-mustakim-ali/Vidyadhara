from fastapi import APIRouter
from controllers import admin_controller

router = APIRouter()

# -----------------------
# User management
# -----------------------
@router.post("/users")
async def add_user(payload: dict):
    return await admin_controller.add_user(payload)

@router.get("/users")
async def list_users():
    return await admin_controller.get_users()

@router.get("/users/students")
async def list_students():
    return await admin_controller.get_students()

@router.get("/users/teachers")
async def list_teachers():
    return await admin_controller.get_teachers()

@router.get("/users/admins")
async def list_admins():
    return await admin_controller.get_admins()

@router.delete("/users/{user_id}")
async def delete_user(user_id: str):   # 🔹 changed to str, since Supabase UUIDs are strings
    return await admin_controller.delete_user(user_id)

# -----------------------
# Gamification rules
# -----------------------
@router.post("/gamification/rules")
async def set_gamification_rules(payload: dict):
    return await admin_controller.set_gamification_rules(payload)

@router.get("/gamification/rules")
async def get_gamification_rules():
    return await admin_controller.get_gamification_rules()

# -----------------------
# Analytics
# -----------------------
@router.get("/analytics")
async def get_analytics():
    return await admin_controller.get_analytics()
