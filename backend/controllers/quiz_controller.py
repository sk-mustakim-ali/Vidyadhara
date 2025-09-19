import os, json, datetime
from config.supabase_client import DATA_DIR
from utils.response import success, error

QUIZZES_FILE = os.path.join(DATA_DIR, "quizzes.json")
ATTEMPTS_FILE = os.path.join(DATA_DIR, "quiz_attempts.json")
RULES_FILE = os.path.join(DATA_DIR, "gamification_rules.json")

os.makedirs(DATA_DIR, exist_ok=True)
for f, default in [(QUIZZES_FILE, []), (ATTEMPTS_FILE, [])]:
    if not os.path.exists(f):
        with open(f, "w") as fh:
            json.dump(default, fh)

async def create_quiz(payload: dict):
    required = ["lesson_id", "questions"]
    for r in required:
        if r not in payload:
            return error(f"missing {r}", 400)
    with open(QUIZZES_FILE, "r") as f:
        quizzes = json.load(f)
    new = {
        "id": str(len(quizzes) + 1),
        "lesson_id": payload["lesson_id"],
        "type": payload.get("type", "mcq"),
        "difficulty": payload.get("difficulty", "medium"),
        "theme": payload.get("theme"),
        # questions: list of {id, text, choices: [..], answer: index_or_value}
        "questions": payload["questions"],
        "created_at": str(datetime.datetime.utcnow())
    }
    quizzes.append(new)
    with open(QUIZZES_FILE, "w") as f:
        json.dump(quizzes, f, indent=2)
    return success(new)

async def quizzes_for_lesson(lesson_id: str):
    with open(QUIZZES_FILE, "r") as f:
        quizzes = json.load(f)
    filtered = [q for q in quizzes if str(q.get("lesson_id")) == str(lesson_id)]
    return success({"quizzes": filtered})

async def get_quiz(quiz_id: str):
    with open(QUIZZES_FILE, "r") as f:
        quizzes = json.load(f)
    quiz = next((q for q in quizzes if str(q["id"]) == str(quiz_id)), None)
    if not quiz:
        return error("quiz not found", 404)
    # return quiz without answers for safety
    safe_questions = []
    for q in quiz["questions"]:
        q_copy = q.copy()
        q_copy.pop("answer", None)
        safe_questions.append(q_copy)
    q_safe = quiz.copy()
    q_safe["questions"] = safe_questions
    return success(q_safe)

async def attempt_quiz(quiz_id: str, payload: dict):
    """
    payload: { student_id, answers: [{question_id, answer}] }
    """
    required = ["student_id", "answers"]
    for r in required:
        if r not in payload:
            return error(f"missing {r}", 400)

    with open(QUIZZES_FILE, "r") as f:
        quizzes = json.load(f)
    quiz = next((q for q in quizzes if str(q["id"]) == str(quiz_id)), None)
    if not quiz:
        return error("quiz not found", 404)

    # compute score
    total = len(quiz["questions"])
    correct = 0
    q_map = {str(q["id"]): q for q in quiz["questions"]}
    for a in payload["answers"]:
        qid = str(a.get("question_id"))
        given = a.get("answer")
        qobj = q_map.get(qid)
        if not qobj:
            continue
        if qobj.get("answer") == given:
            correct += 1

    score = int((correct / total) * 100) if total > 0 else 0

    # store attempt
    with open(ATTEMPTS_FILE, "r") as f:
        attempts = json.load(f)
    attempt = {
        "id": str(len(attempts) + 1),
        "quiz_id": quiz_id,
        "student_id": payload["student_id"],
        "score": score,
        "correct": correct,
        "total": total,
        "completed_at": str(datetime.datetime.utcnow())
    }
    attempts.append(attempt)
    with open(ATTEMPTS_FILE, "w") as f:
        json.dump(attempts, f, indent=2)

    # Award tokens (use rule tokens_per_quiz or fallback)
    tokens = 15
    if os.path.exists(RULES_FILE):
        with open(RULES_FILE, "r") as rf:
            rules = json.load(rf)
            tokens = rules.get("tokens_per_quiz", tokens)

    try:
        from controllers import gamification_controller
        # award tokens proportional to score (rounded)
        token_value = int((score / 100) * tokens)
        if token_value > 0:
            await gamification_controller.add_reward(payload["student_id"], {"type": "token", "value": token_value})
    except Exception as e:
        print("Gamification error:", e)

    return success({"attempt": attempt})
