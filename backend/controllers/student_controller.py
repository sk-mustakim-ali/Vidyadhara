import os, json, datetime
from config.supabase_client import supabase, SUPABASE_AVAILABLE, DATA_DIR
from utils.response import success, error

CONTENT_FILE = os.path.join(DATA_DIR, 'content.json')
PROGRESS_FILE = os.path.join(DATA_DIR, 'progress.json')
ASSIGNMENTS_FILE = os.path.join(DATA_DIR, 'assignments.json')
RULES_FILE = os.path.join(DATA_DIR, 'gamification_rules.json')

# --------------------
# Helpers
# --------------------
def load_rules():
    if os.path.exists(RULES_FILE):
        with open(RULES_FILE, "r") as f:
            return json.load(f)
    return {
        "tokens_per_completed_lesson": 10,
        "tokens_per_completed_homework": 20
    }

async def award_badges(user_id: str):
    """Check milestones and award badges"""
    from controllers import gamification_controller
    badge = await gamification_controller.check_and_award_badges(user_id)
    if badge:
        print(f"🏅 Badge awarded: {badge['value']} to student {user_id}")

# --------------------
# Student Actions
# --------------------
async def get_content():
    """Fetch lessons from DB or fallback to JSON"""
    if SUPABASE_AVAILABLE:
        try:
            response = supabase.table("lessons").select("*").execute()
            return success({"content": response.data})
        except Exception as e:
            return error(str(e), 500)
    else:
        with open(CONTENT_FILE, 'r') as f:
            return success({'content': json.load(f)})


async def save_progress(payload: dict):
    """Track student progress on lessons"""
    required = ['user_id', 'content_id', 'status']
    for r in required:
        if r not in payload:
            return error(f'missing {r}', 400)

    if SUPABASE_AVAILABLE:
        try:
            entry = {
                "student_id": payload['user_id'],
                "lesson_id": payload['content_id'],
                "status": payload['status'],
                "score": payload.get('score'),
                "generated_at": datetime.datetime.utcnow().isoformat()
            }

            response = supabase.table("progress_reports").insert(entry).execute()

            # 🎉 Award gamification rewards
            if payload["status"] == "completed":
                rules = load_rules()
                tokens = rules.get("tokens_per_completed_lesson", 10)
                from controllers import gamification_controller
                await gamification_controller.add_reward(
                    payload["user_id"], {"type": "token", "value": tokens}
                )
                await award_badges(payload["user_id"])

            return success(response.data[0])
        except Exception as e:
            return error(str(e), 500)

    else:
        # JSON fallback
        with open(PROGRESS_FILE, 'r') as f:
            progress = json.load(f)

        entry = {
            'id': len(progress) + 1,
            'user_id': payload['user_id'],
            'content_id': payload['content_id'],
            'status': payload['status'],
            'score': payload.get('score')
        }
        progress.append(entry)

        with open(PROGRESS_FILE, 'w') as f:
            json.dump(progress, f, indent=2)

        return success(entry)


async def submit_homework(assignment_id: str, payload: dict):
    """Student submits homework assigned by teacher"""
    required = ['user_id', 'status']
    for r in required:
        if r not in payload:
            return error(f'missing {r}', 400)

    if SUPABASE_AVAILABLE:
        try:
            # 1. Validate assignment
            assignment = supabase.table("assignments").select("*").eq("id", assignment_id).execute()
            if not assignment.data:
                return error("assignment not found", 404)

            assignment = assignment.data[0]

            # If single-student assignment, validate ownership
            if "student_id" in assignment and assignment['student_id'] != payload['user_id']:
                return error("this assignment does not belong to the student", 403)

            # 2. Insert submission
            submission = {
                "assignment_id": assignment_id,
                "student_id": payload['user_id'],
                "status": payload['status'],
                "score": payload.get('score'),
                "submitted_at": datetime.datetime.utcnow().isoformat()
            }
            response = supabase.table("assignment_submissions").insert(submission).execute()

            # 3. Update assignment status
            supabase.table("assignments").update({"status": "submitted"}).eq("id", assignment_id).execute()

            # 🎉 Gamification
            if payload["status"] == "completed":
                rules = load_rules()
                tokens = rules.get("tokens_per_completed_homework", 20)
                from controllers import gamification_controller
                await gamification_controller.add_reward(
                    payload["user_id"], {"type": "token", "value": tokens}
                )
                await award_badges(payload["user_id"])

            return success({"assignment": assignment, "submission": response.data[0]})
        except Exception as e:
            return error(str(e), 500)

    else:
        # JSON fallback
        with open(ASSIGNMENTS_FILE, 'r') as f:
            assignments = json.load(f)
        assignment = next((a for a in assignments if a['id'] == assignment_id), None)
        if not assignment:
            return error('assignment not found', 404)

        assignment['status'] = 'submitted'
        with open(ASSIGNMENTS_FILE, 'w') as f:
            json.dump(assignments, f, indent=2)

        with open(PROGRESS_FILE, 'r') as f:
            progress = json.load(f)
        submission = {
            'id': len(progress) + 1,
            'user_id': payload['user_id'],
            'content_id': assignment['content_id'],
            'status': payload['status'],
            'score': payload.get('score')
        }
        progress.append(submission)
        with open(PROGRESS_FILE, 'w') as f:
            json.dump(progress, f, indent=2)

        return success({'assignment': assignment, 'submission': submission})
