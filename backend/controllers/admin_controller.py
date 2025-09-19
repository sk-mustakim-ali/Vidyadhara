import os, json
from hashlib import sha256
from config.supabase_client import supabase, SUPABASE_AVAILABLE, DATA_DIR
from utils.response import success, error

USERS_FILE = os.path.join(DATA_DIR, "users.json")
CONTENT_FILE = os.path.join(DATA_DIR, "content.json")
PROGRESS_FILE = os.path.join(DATA_DIR, "progress.json")
RULES_FILE = os.path.join(DATA_DIR, "gamification_rules.json")

# Ensure files exist (fallback)
for f, default in [
    (USERS_FILE, []),
    (CONTENT_FILE, []),
    (PROGRESS_FILE, []),
    (RULES_FILE, {"tokens_per_completed_lesson": 10})
]:
    if not os.path.exists(f):
        with open(f, "w") as file:
            json.dump(default, file)

# -------------------
# USER MANAGEMENT
# -------------------
async def add_user(payload: dict):
    required = ["name", "role"]
    for r in required:
        if r not in payload:
            return error(f"missing {r}", 400)

    if SUPABASE_AVAILABLE:
        try:
            new_user = {
                "name": payload["name"],
                "role": payload["role"],
                "grade": payload.get("grade"),
                "language": payload.get("language"),
                "avatar_config": payload.get("avatar_config", {})
            }
            response = supabase.table("users").insert(new_user).execute()
            return success(response.data[0])
        except Exception as e:
            return error(str(e), 500)
    else:
        with open(USERS_FILE, "r") as f:
            users = json.load(f)

        if any(u["name"].lower() == payload["name"].lower() for u in users):
            return error("user already exists", 400)

        user = {
            "id": len(users) + 1,
            "name": payload["name"],
            "role": payload["role"],
            "grade": payload.get("grade"),
            "language": payload.get("language"),
            "avatar_config": payload.get("avatar_config", {})
        }
        users.append(user)

        with open(USERS_FILE, "w") as f:
            json.dump(users, f, indent=2)

        return success(user)

async def get_users():
    if SUPABASE_AVAILABLE:
        try:
            response = supabase.table("users").select("*").execute()
            return success(response.data)
        except Exception as e:
            return error(str(e), 500)
    else:
        with open(USERS_FILE, "r") as f:
            users = json.load(f)
        return success(users)

async def get_students():
    if SUPABASE_AVAILABLE:
        try:
            response = supabase.table("users").select("*").eq("role", "student").execute()
            return success(response.data)
        except Exception as e:
            return error(str(e), 500)
    else:
        with open(USERS_FILE, "r") as f:
            users = json.load(f)
        return success([u for u in users if u.get("role") == "student"])

async def get_teachers():
    if SUPABASE_AVAILABLE:
        try:
            response = supabase.table("users").select("*").eq("role", "teacher").execute()
            return success(response.data)
        except Exception as e:
            return error(str(e), 500)
    else:
        with open(USERS_FILE, "r") as f:
            users = json.load(f)
        return success([u for u in users if u.get("role") == "teacher"])

async def get_admins():
    if SUPABASE_AVAILABLE:
        try:
            response = supabase.table("users").select("*").eq("role", "admin").execute()
            return success(response.data)
        except Exception as e:
            return error(str(e), 500)
    else:
        with open(USERS_FILE, "r") as f:
            users = json.load(f)
        return success([u for u in users if u.get("role") == "admin"])

async def delete_user(user_id: str):
    if SUPABASE_AVAILABLE:
        try:
            supabase.table("users").delete().eq("id", user_id).execute()
            return success({"deleted_user_id": user_id})
        except Exception as e:
            return error(str(e), 500)
    else:
        with open(USERS_FILE, "r") as f:
            users = json.load(f)
        users = [u for u in users if u["id"] != user_id]
        with open(USERS_FILE, "w") as f:
            json.dump(users, f, indent=2)
        return success({"deleted_user_id": user_id})

# -------------------
# GAMIFICATION RULES
# -------------------
async def set_gamification_rules(payload: dict):
    with open(RULES_FILE, "w") as f:
        json.dump(payload, f, indent=2)
    return success(payload)

async def get_gamification_rules():
    with open(RULES_FILE, "r") as f:
        rules = json.load(f)
    return success(rules)

# -------------------
# ANALYTICS
# -------------------
async def get_analytics():
    if SUPABASE_AVAILABLE:
        try:
            users = supabase.table("users").select("*").execute().data
            lessons = supabase.table("lessons").select("*").execute().data
            submissions = supabase.table("assignment_submissions").select("*").execute().data

            stats = {
                "total_users": len(users),
                "students": len([u for u in users if u["role"] == "student"]),
                "teachers": len([u for u in users if u["role"] == "teacher"]),
                "admins": len([u for u in users if u["role"] == "admin"]),
                "total_lessons": len(lessons),
                "total_submissions": len(submissions)
            }
            return success(stats)
        except Exception as e:
            return error(str(e), 500)
    else:
        with open(USERS_FILE, "r") as f:
            users = json.load(f)
        with open(CONTENT_FILE, "r") as f:
            content = json.load(f)
        with open(PROGRESS_FILE, "r") as f:
            progress = json.load(f)

        stats = {
            "total_users": len(users),
            "students": len([u for u in users if u["role"] == "student"]),
            "teachers": len([u for u in users if u["role"] == "teacher"]),
            "admins": len([u for u in users if u["role"] == "admin"]),
            "total_lessons": len(content),
            "total_submissions": len(progress)
        }
        return success(stats)
