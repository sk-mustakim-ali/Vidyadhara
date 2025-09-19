import os, json, datetime
from config.supabase_client import DATA_DIR
from utils.response import success, error

CHALLENGES_FILE = os.path.join(DATA_DIR, "challenges.json")
STUDENT_CH_FILE = os.path.join(DATA_DIR, "student_challenges.json")
os.makedirs(DATA_DIR, exist_ok=True)
for f, default in [(CHALLENGES_FILE, []), (STUDENT_CH_FILE, [])]:
    if not os.path.exists(f):
        with open(f, "w") as fh:
            json.dump(default, fh)

async def create_challenge(payload: dict):
    required = ["title", "duration_minutes", "reward_tokens"]
    for r in required:
        if r not in payload:
            return error(f"missing {r}", 400)
    with open(CHALLENGES_FILE, "r") as f:
        challenges = json.load(f)
    new = {
        "id": str(len(challenges) + 1),
        "title": payload["title"],
        "description": payload.get("description", ""),
        "duration_minutes": payload["duration_minutes"],
        "reward_tokens": payload["reward_tokens"],
        "created_at": str(datetime.datetime.utcnow())
    }
    challenges.append(new)
    with open(CHALLENGES_FILE, "w") as f:
        json.dump(challenges, f, indent=2)
    return success(new)

async def list_challenges():
    with open(CHALLENGES_FILE, "r") as f:
        challenges = json.load(f)
    return success({"challenges": challenges})

async def join_challenge(payload: dict):
    required = ["student_id", "challenge_id"]
    for r in required:
        if r not in payload:
            return error(f"missing {r}", 400)
    with open(STUDENT_CH_FILE, "r") as f:
        sc = json.load(f)
    # prevent duplicate join
    if any(s["student_id"] == payload["student_id"] and s["challenge_id"] == payload["challenge_id"] for s in sc):
        return error("already joined", 400)
    entry = {
        "student_id": payload["student_id"],
        "challenge_id": payload["challenge_id"],
        "status": "in_progress",
        "joined_at": str(datetime.datetime.utcnow())
    }
    sc.append(entry)
    with open(STUDENT_CH_FILE, "w") as f:
        json.dump(sc, f, indent=2)
    return success(entry)

async def complete_challenge(payload: dict):
    required = ["student_id", "challenge_id"]
    for r in required:
        if r not in payload:
            return error(f"missing {r}", 400)

    with open(CHALLENGES_FILE, "r") as f:
        challenges = json.load(f)
    challenge = next((c for c in challenges if str(c["id"]) == str(payload["challenge_id"])), None)
    if not challenge:
        return error("challenge not found", 404)

    with open(STUDENT_CH_FILE, "r") as f:
        sc = json.load(f)

    entry = next((s for s in sc if s["student_id"] == payload["student_id"] and s["challenge_id"] == payload["challenge_id"]), None)
    if not entry:
        return error("student not enrolled in challenge", 400)

    entry["status"] = "completed"
    entry["completed_at"] = str(datetime.datetime.utcnow())

    with open(STUDENT_CH_FILE, "w") as f:
        json.dump(sc, f, indent=2)

    # award tokens using gamification_controller if present
    try:
        from controllers import gamification_controller
        await gamification_controller.add_reward(payload["student_id"], {"type": "token", "value": int(challenge.get("reward_tokens", 0))})
    except Exception as e:
        print("Gamification awarding error:", e)

    return success({"challenge": challenge, "student_challenge": entry})
