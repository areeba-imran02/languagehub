# Testing

## Backend

From the repository root:

```bash
python -m pip install -r backend/requirements.txt
PYTHONPATH=backend python -m pytest -q tests
python -m compileall -q backend ai_engine
```

The automated backend suite uses an isolated SQLite database and currently passes 10 tests. It covers health, registration/login, authenticated vocabulary, authentication enforcement, AI missing-key behavior, curriculum checks, answer-key privacy, and progress validation/summary. Gemini integration is not a live external test.

## Database migrations

From `backend/` with the target `DATABASE_URL` configured:

```bash
alembic upgrade head
alembic current
```

The initial migration was locally verified with SQLite using upgrade, downgrade, and upgrade. Validate PostgreSQL migrations against your own staging database before production.

## Web and mobile

Install dependencies in `apps/web` and `apps/mobile`, then run:

```bash
# apps/web
npm install
npm run typecheck
npm run build

# apps/mobile
npm install
npm run typecheck
```

npm dependency installation timed out in the build environment, so these Node checks have not been claimed as locally passing. The included GitHub Actions workflow runs the web typecheck/build and mobile typecheck after push or pull request. Expo emulator, physical-device, and signed store builds still require a real device/build environment.
