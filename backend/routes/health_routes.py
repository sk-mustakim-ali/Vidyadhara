from fastapi import APIRouter
from config.supabase_client import SUPABASE_AVAILABLE, supabase

router = APIRouter()

@router.get("/db")
async def db_health():
    if not SUPABASE_AVAILABLE:
        return {"status": "error", "message": "Supabase not configured"}
    
    try:
        # Simple query → check if users table exists
        response = supabase.table("users").select("id").limit(1).execute()
        return {"status": "ok", "message": "Database connected", "rows": len(response.data)}
    except Exception as e:
        return {"status": "error", "message": str(e)}
