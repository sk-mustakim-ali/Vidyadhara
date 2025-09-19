from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Existing routes
from routes import (
    auth_routes,
    student_routes,
    teacher_routes,
    gamification_routes,
    admin_routes,
    analytics_routes,
    sync_routes,
    subject_routes,
    notes_routes,
    challenge_routes,
    quiz_routes,
    ai_routes,
    health_routes   # ⬅️ NEW health check
)

app = FastAPI(title='Vidyadhara Backend Prototype')

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Register routes
app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
app.include_router(student_routes.router, prefix="/student", tags=["student"])
app.include_router(teacher_routes.router, prefix="/teacher", tags=["teacher"])
app.include_router(gamification_routes.router, prefix="/gamification", tags=["gamification"])
app.include_router(admin_routes.router, prefix="/admin", tags=["admin"])
app.include_router(analytics_routes.router, prefix="/analytics", tags=["analytics"])
app.include_router(sync_routes.router, prefix="/sync", tags=["sync"])
app.include_router(subject_routes.router, prefix="/subjects", tags=["subjects"])
app.include_router(notes_routes.router, prefix="/notes", tags=["notes"])
app.include_router(challenge_routes.router, prefix="/challenges", tags=["challenges"])
app.include_router(quiz_routes.router, prefix="/quizzes", tags=["quizzes"])
app.include_router(ai_routes.router, prefix="/ai", tags=["ai"])
app.include_router(health_routes.router, prefix="/health", tags=["health"])  # ⬅️ DB health check

@app.get('/')
def root():
    return {'status': 'ok', 'service': 'vidyadhara-prototype'}

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
