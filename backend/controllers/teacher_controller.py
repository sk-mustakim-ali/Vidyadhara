from config.supabase_client import supabase, SUPABASE_AVAILABLE, DATA_DIR
from utils.response import success, error
import os, json

CONTENT_FILE = os.path.join(DATA_DIR, "content.json")
ASSIGNMENTS_FILE = os.path.join(DATA_DIR, "assignments.json")
SUBMISSIONS_FILE = os.path.join(DATA_DIR, "progress.json")

# --------------------
# Teacher Actions
# --------------------

async def add_content(payload: dict):
    """Teacher adds a lesson (DB = lessons table)"""
    required = ["subject_id", "grade", "content_url"]
    for r in required:
        if r not in payload:
            return error(f"missing {r}", 400)

    if SUPABASE_AVAILABLE:
        try:
            new_item = {
                "subject_id": payload["subject_id"],
                "grade": payload["grade"],
                "content_url": payload["content_url"],
                "story_mode": payload.get("story_mode", False),
                "interactive": payload.get("interactive", False),
            }
            response = supabase.table("lessons").insert(new_item).execute()
            return success(response.data[0])
        except Exception as e:
            return error(str(e), 500)
    else:
        return error("Supabase not available (JSON fallback removed for lessons)", 500)


async def create_homework(payload: dict):
    """Teacher assigns homework (DB = assignments table)"""
    required = ["teacher_id", "lesson_id"]
    for r in required:
        if r not in payload:
            return error(f"missing {r}", 400)

    if SUPABASE_AVAILABLE:
        try:
            new_assignment = {
                "teacher_id": payload["teacher_id"],
                "lesson_id": payload["lesson_id"],
                "type": payload.get("type", "homework"),
                "due_date": payload.get("due_date"),
                "offline_available": payload.get("offline_available", False),
            }
            response = supabase.table("assignments").insert(new_assignment).execute()
            return success(response.data[0])
        except Exception as e:
            return error(str(e), 500)
    else:
        return error("Supabase not available (JSON fallback removed for assignments)", 500)


async def get_submissions():
    """Teacher views student submissions (DB = assignment_submissions)"""
    if SUPABASE_AVAILABLE:
        try:
            response = supabase.table("assignment_submissions").select("*").execute()
            return success({"submissions": response.data})
        except Exception as e:
            return error(str(e), 500)
    else:
        return error("Supabase not available (JSON fallback removed for submissions)", 500)
