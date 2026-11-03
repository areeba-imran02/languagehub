# API overview

Base path: `/api/v1` (except `/health`). Interactive OpenAPI documentation is served at `/docs`.

- `POST /auth/register` — create learner account
- `POST /auth/login` — obtain bearer token
- `GET /auth/me` — current user
- `GET /languages` — supported language registry
- `GET/POST /vocabulary` — list and save current user's words
- `DELETE /vocabulary/{word_id}` — delete an owned word
- `GET/POST /progress` — read summary and record activity
- `POST /ai/tutor` — Gemini-backed tutor; returns 503 when unconfigured/unavailable
- `GET /courses`, `GET /courses/{course_id}/lessons` — course catalog
- `GET /admin/overview` — admin-only overview

All private endpoints require `Authorization: Bearer <token>`. Request and response schemas are defined in `backend/app/schemas.py`.
