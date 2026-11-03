# Installation

## Requirements
- Python 3.11+ (tested in this workspace with Python 3.13)
- Node.js 20+
- PostgreSQL 15+ for production; SQLite is used by default locally
- A Gemini API key for live tutor responses

## Backend
From `backend/`: create/activate a virtual environment, `pip install -r requirements.txt`, copy root `.env.example` to `backend/.env`, then run `uvicorn app.main:app --reload`. The backend creates local tables on startup. For controlled deployments, use Alembic migrations (`alembic upgrade head`).

## Web and mobile
Install dependencies independently in `apps/web` and `apps/mobile`. Copy each `.env.example` to the respective local env file. Mobile devices must use a LAN-reachable backend host, not `localhost`.
