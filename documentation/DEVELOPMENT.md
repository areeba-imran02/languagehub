# Development

The monorepo separates web, mobile, backend, AI orchestration, curriculum, infrastructure, and tests. Backend routes are versioned under `/api/v1`. Keep Gemini credentials on the backend. Add schema changes to SQLAlchemy models and Alembic revisions. Use per-user ownership filters for every private resource.

Suggested workflow: run backend tests, run the backend, verify `/health` and `/docs`, start web, then start Expo. Avoid committing `.env` files or generated build output.
