# LanguageHub — Start Here

This is the single project folder to extract and upload to GitHub. It contains the backend, web app, Expo mobile starter, AI prompt/adapter code, curriculum data, database migration, CI workflow, tests, and setup/deployment documentation.

> **Important:** This is a working development foundation, not a finished production SaaS. Backend tests pass (10/10). Web and mobile dependency installation timed out here, so their local typechecks/builds are not verified. GitHub Actions is configured to run web typecheck/build and mobile typecheck after you push. See `documentation/IMPLEMENTATION_STATUS.md` for the exact feature-by-feature status.

## 1. Requirements

- Python 3.11 or newer
- Node.js 20 or newer and npm
- Git (for GitHub upload)
- Optional: Docker Desktop (for PostgreSQL)
- Optional: Gemini API key (for live AI tutor responses)

## 2. Start the backend (Windows PowerShell)

Open PowerShell in the extracted `LanguageHub` folder and run:

```powershell
cd backend
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item ..\.env.example .env
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` to explore the API and `http://127.0.0.1:8000/health` to check health. The default local database is SQLite and is created automatically.

For live AI tutor use, open `backend/.env` and set `GEMINI_API_KEY` to your own key. Keep that key private; never put it in the web or mobile environment files or commit it to GitHub.

## 3. Start the web app

Open a second terminal in the project root:

```powershell
cd apps/web
npm install
Copy-Item .env.example .env.local
npm run dev
```

Open `http://localhost:3000`. Confirm `NEXT_PUBLIC_API_URL` in `apps/web/.env.local` is `http://localhost:8000/api/v1` for local development.

## 4. Start the mobile app

Open a third terminal:

```powershell
cd apps/mobile
npm install
Copy-Item .env.example .env
npx expo start
```

Set `EXPO_PUBLIC_API_URL` to an address the phone/emulator can reach. A physical phone cannot normally reach the development computer through `localhost`; use the computer's LAN IP and ensure both devices share the network.

## 5. Run backend tests

From the project root:

```powershell
python -m pip install -r backend/requirements.txt
$env:PYTHONPATH = "backend"
python -m pytest -q tests
```

## 6. Upload to GitHub

1. Extract this ZIP.
2. Create an empty repository on GitHub.
3. Upload the **contents** of the extracted `LanguageHub` folder, or use GitHub Desktop to publish that folder.
4. Do not upload `.env`, `.env.local`, API keys, database files, `node_modules`, or build folders. The included `.gitignore` excludes common local-only files.
5. After pushing, open the repository's **Actions** tab and check the CI workflow result.

Detailed instructions: `documentation/GITHUB_UPLOAD.md`.

## 7. Deployment and next implementation work

Deployment guidance is in `documentation/DEPLOYMENT.md`. Before a public production launch, complete the remaining items in `documentation/IMPLEMENTATION_STATUS.md`, including full authentication lifecycle, production database configuration/migrations, persisted end-to-end learning flows, admin workflows, speech/audio integrations, security hardening, and successful web/mobile build and integration tests.
