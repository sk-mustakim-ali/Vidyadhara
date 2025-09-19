import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Debug print to confirm env variables
print("DEBUG: SUPABASE_URL =", os.getenv("SUPABASE_URL"))
print("DEBUG: APP_SECRET =", os.getenv("APP_SECRET"))
print("DEBUG: GEMINI_API_KEY starts with =", str(os.getenv("GEMINI_API_KEY"))[:8])

SUPABASE_URL = os.getenv('SUPABASE_URL') or ''
SUPABASE_KEY = os.getenv('SUPABASE_KEY') or ''
APP_SECRET = os.getenv('APP_SECRET') or 'demo-secret'

SUPABASE_AVAILABLE = False
supabase = None

if SUPABASE_URL and SUPABASE_KEY:
    try:
        from supabase import create_client
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        SUPABASE_AVAILABLE = True
    except Exception:
        SUPABASE_AVAILABLE = False

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(DATA_DIR, exist_ok=True)
