# Vidyadhara Backend Prototype (FastAPI)

Minimal prototype backend for Vidyadhara using FastAPI.

## Features
- /auth/signup and /auth/login
- /student/content and /student/progress
- Supabase integration ready (fallback to local JSON if not configured)

## Run Instructions
1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # on Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and fill with Supabase credentials (or leave blank for local fallback).

3. Start the server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

4. Open docs at http://localhost:8000/docs
