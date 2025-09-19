import os, json, datetime
from config.supabase_client import DATA_DIR
from utils.response import success, error

NOTES_FILE = os.path.join(DATA_DIR, "notes.json")
os.makedirs(DATA_DIR, exist_ok=True)
if not os.path.exists(NOTES_FILE):
    with open(NOTES_FILE, "w") as f:
        json.dump([], f)

async def get_notes_for_lesson(lesson_id: str):
    with open(NOTES_FILE, "r") as f:
        notes = json.load(f)
    filtered = [n for n in notes if str(n.get("lesson_id")) == str(lesson_id)]
    return success({"notes": filtered})

async def add_note(payload: dict):
    required = ["lesson_id", "created_by"]
    for r in required:
        if r not in payload:
            return error(f"missing {r}", 400)
    with open(NOTES_FILE, "r") as f:
        notes = json.load(f)
    new = {
        "id": str(len(notes) + 1),
        "lesson_id": payload["lesson_id"],
        "created_by": payload["created_by"],
        "text": payload.get("text", ""),
        "file_url": payload.get("file_url"),
        "created_at": str(datetime.datetime.utcnow())
    }
    notes.append(new)
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f, indent=2)
    return success(new)

async def delete_note(note_id: str):
    with open(NOTES_FILE, "r") as f:
        notes = json.load(f)
    notes = [n for n in notes if str(n.get("id")) != str(note_id)]
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f, indent=2)
    return success({"deleted_note_id": note_id})
