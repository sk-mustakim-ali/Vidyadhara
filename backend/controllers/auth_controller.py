import hashlib, hmac, os, json
from config.supabase_client import APP_SECRET, DATA_DIR
from utils.response import success, error

USERS_FILE = os.path.join(DATA_DIR, 'users.json')
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, 'w') as f:
        json.dump([], f)

async def _hash_password(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

async def _read_users():
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

async def _write_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

async def signup(payload: dict):
    required = ['email', 'password', 'role']
    for r in required:
        if r not in payload:
            return error(f'missing {r}', 400)
    email = payload['email'].lower()
    users = await _read_users()
    if any(u['email'] == email for u in users):
        return error('user already exists', 400)
    user = {
        'id': len(users) + 1,
        'email': email,
        'role': payload['role'],
        'password_hash': await _hash_password(payload['password'])
    }
    users.append(user)
    await _write_users(users)
    return success({'id': user['id'], 'email': user['email'], 'role': user['role']})

async def login(payload: dict):
    required = ['email', 'password']
    for r in required:
        if r not in payload:
            return error(f'missing {r}', 400)
    email = payload['email'].lower()
    pw_hash = await _hash_password(payload['password'])
    users = await _read_users()
    user = next((u for u in users if u['email'] == email and u['password_hash'] == pw_hash), None)
    if not user:
        return error('invalid credentials', 401)
    token = hmac.new(APP_SECRET.encode(), email.encode(), 'sha256').hexdigest()
    return success({'token': token, 'id': user['id'], 'role': user['role']})
