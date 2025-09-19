from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os, asyncio
from backend.config.supabase_client import DATA_DIR
from backend.controllers.ai_controller import ai_chat  # ✅ Import added


  # ✅ Import your AI controller

app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app)

# -------------------------
#  HOME ROUTE
# -------------------------
@app.route("/")
def home():
    return send_from_directory(".", "login.html")

# -------------------------
#  LOGIN ROUTE
# -------------------------
@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    role = data.get("role")

    # Simple demo validation
    if username == "admin" and password == "123" and role == "admin":
        return jsonify({"success": True, "redirect": "admin.html"})
    elif username == "teacher" and password == "123" and role == "teacher":
        return jsonify({"success": True, "redirect": "teacher.html"})
    elif username == "student" and password == "123" and role == "student":
        return jsonify({"success": True, "redirect": "student.html"})
    else:
        return jsonify({"success": False, "message": "Invalid credentials"})

# -------------------------
#  SAMPLE DATA ENDPOINTS
# -------------------------
@app.route("/api/teachers", methods=["GET"])
def get_teachers():
    return jsonify([
        {"id": 1, "name": "Mr. A", "email": "a@school.com", "subject": "Math", "status": "Active"},
        {"id": 2, "name": "Ms. B", "email": "b@school.com", "subject": "Science", "status": "Inactive"}
    ])

@app.route("/api/students", methods=["GET"])
def get_students():
    return jsonify([
        {"id": 1, "name": "Priya", "email": "priya@school.com", "grade": "10", "status": "Active"},
        {"id": 2, "name": "Rahul", "email": "rahul@school.com", "grade": "12", "status": "Inactive"}
    ])

# -------------------------
#  CHATBOT ENDPOINT
# -------------------------
@app.route("/chat", methods=["POST"])
def chat():
    payload = request.get_json()
    if not payload:
        return jsonify({"error": "Missing request body"}), 400

    try:
        # ai_chat is async → run inside event loop
        result = asyncio.run(ai_chat(payload))
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------------
#  MAIN
# -------------------------
if __name__ == "__main__":
    app.run(port=5000, debug=True)