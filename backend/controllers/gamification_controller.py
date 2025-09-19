import os, json
from config.supabase_client import DATA_DIR
from utils.response import success, error

REWARDS_FILE = os.path.join(DATA_DIR, "rewards.json")
LEADERBOARD_FILE = os.path.join(DATA_DIR, "leaderboard.json")
PROGRESS_FILE = os.path.join(DATA_DIR, "progress.json")

# Ensure files exist
for f in [REWARDS_FILE, LEADERBOARD_FILE, PROGRESS_FILE]:
    if not os.path.exists(f):
        with open(f, "w") as file:
            json.dump([], file)

# --------------------------
# Leaderboard & Rewards
# --------------------------
async def get_leaderboard():
    with open(LEADERBOARD_FILE, "r") as f:
        leaderboard = json.load(f)
    # Sort by tokens descending
    leaderboard = sorted(leaderboard, key=lambda x: x.get("tokens", 0), reverse=True)
    return success({"leaderboard": leaderboard})

async def get_rewards(student_id: int):
    with open(REWARDS_FILE, "r") as f:
        rewards = json.load(f)
    user_rewards = [r for r in rewards if r["student_id"] == student_id]
    return success({"rewards": user_rewards})

async def add_reward(student_id: int, payload: dict):
    """Manually or automatically add a reward (badge or token)"""
    if "type" not in payload:
        return error("missing reward type", 400)

    with open(REWARDS_FILE, "r") as f:
        rewards = json.load(f)

    reward = {
        "id": len(rewards) + 1,
        "student_id": student_id,
        "type": payload["type"],   # e.g., "badge_bronze", "token"
        "value": payload.get("value", 1)
    }
    rewards.append(reward)

    with open(REWARDS_FILE, "w") as f:
        json.dump(rewards, f, indent=2)

    # Update leaderboard tokens if reward is token
    if reward["type"] == "token":
        with open(LEADERBOARD_FILE, "r") as f:
            leaderboard = json.load(f)
        user = next((u for u in leaderboard if u["student_id"] == student_id), None)
        if not user:
            leaderboard.append({"student_id": student_id, "tokens": reward["value"]})
        else:
            user["tokens"] = user.get("tokens", 0) + reward["value"]
        with open(LEADERBOARD_FILE, "w") as f:
            json.dump(leaderboard, f, indent=2)

    return success(reward)

# --------------------------
# Badge System
# --------------------------
async def check_and_award_badges(student_id: int):
    """Check milestones and award badges automatically based on completed lessons"""
    # Load student progress
    with open(PROGRESS_FILE, "r") as f:
        progress = json.load(f)
    completed_lessons = len([p for p in progress if p["user_id"] == student_id and p["status"] == "completed"])

    # Load existing rewards
    with open(REWARDS_FILE, "r") as f:
        rewards = json.load(f)

    # Already earned badges
    earned = [r["type"] for r in rewards if r["student_id"] == student_id and r["type"].startswith("badge")]

    new_badge = None
    if completed_lessons >= 20 and "badge_gold" not in earned:
        new_badge = {"id": len(rewards) + 1, "student_id": student_id, "type": "badge_gold", "value": "Gold Learner"}
    elif completed_lessons >= 10 and "badge_silver" not in earned:
        new_badge = {"id": len(rewards) + 1, "student_id": student_id, "type": "badge_silver", "value": "Silver Learner"}
    elif completed_lessons >= 5 and "badge_bronze" not in earned:
        new_badge = {"id": len(rewards) + 1, "student_id": student_id, "type": "badge_bronze", "value": "Bronze Learner"}

    if new_badge:
        rewards.append(new_badge)
        with open(REWARDS_FILE, "w") as f:
            json.dump(rewards, f, indent=2)
        return new_badge

    return None
