import os, json
from config.supabase_client import supabase, SUPABASE_AVAILABLE, DATA_DIR
from utils.response import success, error

SUBJECTS_FILE = os.path.join(DATA_DIR, "subjects.json")
LESSONS_FILE = os.path.join(DATA_DIR, "content.json")  # existing lessons file

os.makedirs(DATA_DIR, exist_ok=True)
if not os.path.exists(SUBJECTS_FILE):
    with open(SUBJECTS_FILE, "w") as f:
        json.dump([], f)

# -------------------
# LIST ALL SUBJECTS
# -------------------
async def list_subjects():
    if SUPABASE_AVAILABLE:
        data = supabase.table("subjects").select("*").execute()
        return success({"subjects": data.data})
    # fallback to JSON
    with open(SUBJECTS_FILE, "r") as f:
        subjects = json.load(f)
    return success({"subjects": subjects})

# -------------------
# CREATE NEW SUBJECT
# -------------------
async def create_subject(payload: dict):
    required = ["name"]
    for r in required:
        if r not in payload:
            return error(f"missing {r}", 400)

    new_subject = {
        "name": payload["name"],
        "description": payload.get("description", "")
    }

    if SUPABASE_AVAILABLE:
        try:
            res = supabase.table("subjects").insert(new_subject).execute()
            new_subject["id"] = res.data[0]["id"]  # get generated id
            return success(new_subject)
        except Exception as e:
            if "duplicate key value" in str(e):
                return error(f"Subject '{payload['name']}' already exists.", 409)
            return error(str(e), 500)

    # fallback to JSON
    with open(SUBJECTS_FILE, "r") as f:
        subjects = json.load(f)
    new_subject["id"] = str(len(subjects) + 1)
    subjects.append(new_subject)
    with open(SUBJECTS_FILE, "w") as f:
        json.dump(subjects, f, indent=2)
    return success(new_subject)


# -------------------
# LESSONS BY SUBJECT
# -------------------
async def lessons_by_subject(subject_id: str):
    if SUPABASE_AVAILABLE:
        data = supabase.table("lessons").select("*").eq("subject_id", subject_id).execute()
        return success({"lessons": data.data})

    # fallback to JSON
    with open(LESSONS_FILE, "r") as f:
        lessons = json.load(f)
    filtered = [l for l in lessons if str(l.get("subject_id")) == str(subject_id)]
    return success({"lessons": filtered})
