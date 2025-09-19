import os, datetime, json
import google.generativeai as genai
from backend.config.supabase_client import DATA_DIR

# ✅ Define success/error helpers here (no need for utils.response)
def success(data, status=200):
    return {"status": "success", "data": data, "status_code": status}

def error(message, status=400):
    return {"status": "error", "message": message, "status_code": status}

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

AI_INTERACTIONS_FILE = os.path.join(DATA_DIR, "ai_interactions.json")

async def ai_chat(payload: dict):
    query = payload.get("query")
    user_id = payload.get("user_id")

    if not query or not user_id:
        return error("missing query or user_id", 400)

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(query)

        # Debug raw response
        print("Gemini raw response:", response)

        # Extract reply safely
        reply = None
        if hasattr(response, "text") and response.text:
            reply = response.text
        elif hasattr(response, "candidates") and response.candidates:
            parts = response.candidates[0].content.parts
            reply = "".join(
                part.text for part in parts if hasattr(part, "text")
            )

        if not reply:
            reply = "⚠️ AI did not return a valid response."

    except Exception as e:
        return error(f"Gemini service error: {str(e)}", 500)

    # Save interaction
    try:
        if os.path.exists(AI_INTERACTIONS_FILE):
            with open(AI_INTERACTIONS_FILE, "r") as f:
                interactions = json.load(f)
        else:
            interactions = []
    except Exception:
        interactions = []

    new = {
        "id": str(len(interactions) + 1),
        "user_id": user_id,
        "query_text": query,
        "response_text": reply,
        "escalated_to_teacher": False,
        "created_at": str(datetime.datetime.utcnow())
    }
    interactions.append(new)

    os.makedirs(os.path.dirname(AI_INTERACTIONS_FILE), exist_ok=True)
    with open(AI_INTERACTIONS_FILE, "w") as f:
        json.dump(interactions, f, indent=2)

    return success(new)
