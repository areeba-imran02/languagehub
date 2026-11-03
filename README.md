# LanguageHub

**One Platform. Every Language. Endless Possibilities.**

LanguageHub is a multilingual learning platform monorepo containing a FastAPI backend, Next.js web app, Expo mobile app, curriculum-backed grammar and reading practice, vocabulary/progress APIs, Gemini-ready AI tutor, focused agent prompt builders, PostgreSQL Docker configuration, Alembic migrations, CI workflow, and documentation.

> **Honest status:** this is an actively developed foundation, not yet the complete production product in the master specification. Read `documentation/IMPLEMENTATION_STATUS.md`. Web and mobile Node checks still need GitHub Actions execution because npm installation timed out in this environment. Live Gemini, hosted PostgreSQL, production deployment, speech features, and app-store builds require external credentials/services and further implementation.

## Quick start — backend (Windows PowerShell)

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item ..\.env.example .env
uvicorn app.main:app --reload
```

API docs: http://127.0.0.1:8000/docs. Local default database: SQLite. For PostgreSQL, start `docker compose -f infrastructure/docker-compose.yml up -d` from the repository root and set `DATABASE_URL` in `backend/.env` to `postgresql+psycopg://languagehub:change-me-local-only@localhost:5432/languagehub` (`psycopg[binary]` is included in backend requirements).

## Web

```powershell
cd apps/web
npm install
Copy-Item .env.example .env.local
npm run dev
```

Open http://localhost:3000. Configure `NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1`.

## Mobile

```powershell
cd apps/mobile
npm install
npx expo start
```

Set `EXPO_PUBLIC_API_URL` to a backend URL reachable from the phone/emulator. `localhost` on a physical phone refers to the phone, not the development PC.

## Tests

```bash
pip install -r backend/requirements.txt
PYTHONPATH=backend pytest -q tests
```

## GitHub

Upload the extracted `LanguageHub` directory contents (not the ZIP itself) to a new GitHub repository. `.gitignore` excludes credentials, virtual environments, dependencies, caches, build outputs and local databases. Never commit a real `.env` or API key.
