import os, json
from config.supabase_client import DATA_DIR
from utils.response import success

USERS_FILE = os.path.join(DATA_DIR, "users.json")
CONTENT_FILE = os.path.join(DATA_DIR, "content.json")
PROGRESS_FILE = os.path.join(DATA_DIR, "progress.json")
ASSIGNMENTS_FILE = os.path.join(DATA_DIR, "assignments.json")

# --------------------
# Student Report
# --------------------
async def get_student_report(student_id: int):
    with open(USERS_FILE, "r") as f:
        users = json.load(f)
    with open(PROGRESS_FILE, "r") as f:
        progress = json.load(f)

    student = next((u for u in users if u["id"] == student_id and u["role"] == "student"), None)
    if not student:
        return success({"error": "student not found"})

    student_progress = [p for p in progress if p["user_id"] == student_id]

    report = {
        "student_id": student_id,
        "email": student["email"],
        "total_lessons_done": len([p for p in student_progress if p["status"] == "completed"]),
        "total_in_progress": len([p for p in student_progress if p["status"] == "in_progress"]),
        "average_score": round(
            sum([p.get("score", 0) or 0 for p in student_progress]) / len(student_progress),
            2
        ) if student_progress else 0
    }
    return success(report)

# --------------------
# Teacher Class Report
# --------------------
async def get_class_report(teacher_id: int):
    with open(USERS_FILE, "r") as f:
        users = json.load(f)
    with open(ASSIGNMENTS_FILE, "r") as f:
        assignments = json.load(f)
    with open(PROGRESS_FILE, "r") as f:
        progress = json.load(f)

    # Get students assigned by this teacher
    teacher_assignments = [a for a in assignments if a["teacher_id"] == teacher_id]
    student_ids = list({a["student_id"] for a in teacher_assignments})
    students = [u for u in users if u["id"] in student_ids]

    class_stats = []
    for student in students:
        student_progress = [p for p in progress if p["user_id"] == student["id"]]
        class_stats.append({
            "student_id": student["id"],
            "email": student["email"],
            "completed": len([p for p in student_progress if p["status"] == "completed"]),
            "pending": len([a for a in teacher_assignments if a["student_id"] == student["id"] and a["status"] != "submitted"])
        })

    report = {
        "teacher_id": teacher_id,
        "students": class_stats,
        "total_students": len(students),
        "total_assignments": len(teacher_assignments)
    }
    return success(report)
