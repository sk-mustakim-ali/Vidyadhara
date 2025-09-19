import os, json, datetime
from config.supabase_client import DATA_DIR
from utils.response import success, error

PROGRESS_FILE = os.path.join(DATA_DIR, "progress.json")
ASSIGNMENTS_FILE = os.path.join(DATA_DIR, "assignments.json")
CONTENT_FILE = os.path.join(DATA_DIR, "content.json")

# --------------------
# Upload Offline Data
# --------------------
async def upload_offline_data(payload: dict):
    """
    Payload format:
    {
      "student_id": 1,
      "progress": [ { content_id, status, score } ],
      "submissions": [ { assignment_id, status, score } ]
    }
    """
    required = ["student_id"]
    for r in required:
        if r not in payload:
            return error(f"missing {r}", 400)

    student_id = payload["student_id"]

    # Save progress
    if "progress" in payload:
        with open(PROGRESS_FILE, "r") as f:
            progress = json.load(f)
        for p in payload["progress"]:
            entry = {
                "id": len(progress) + 1,
                "user_id": student_id,
                "content_id": p["content_id"],
                "status": p.get("status", "completed"),
                "score": p.get("score"),
                "synced_at": str(datetime.datetime.utcnow())
            }
            progress.append(entry)
        with open(PROGRESS_FILE, "w") as f:
            json.dump(progress, f, indent=2)

    # Update assignments submissions
    if "submissions" in payload:
        with open(ASSIGNMENTS_FILE, "r") as f:
            assignments = json.load(f)
        for s in payload["submissions"]:
            for a in assignments:
                if a["id"] == s["assignment_id"] and a["student_id"] == student_id:
                    a["status"] = s.get("status", "submitted")
        with open(ASSIGNMENTS_FILE, "w") as f:
            json.dump(assignments, f, indent=2)

    return success({"message": "offline data synced", "student_id": student_id})

# --------------------
# Download Latest Data
# --------------------
async def download_data(student_id: int):
    """Provide lessons + assignments for offline use"""
    with open(CONTENT_FILE, "r") as f:
        content = json.load(f)
    with open(ASSIGNMENTS_FILE, "r") as f:
        assignments = json.load(f)

    student_assignments = [a for a in assignments if a["student_id"] == student_id]

    return success({
        "lessons": content,
        "assignments": student_assignments
    })
