# Deployment

Deploy FastAPI behind HTTPS with a managed PostgreSQL database. Set a strong random `SECRET_KEY`, restrict `CORS_ORIGINS`, configure database TLS, run Alembic migrations, and supply Gemini credentials via the platform secret manager. Deploy Next.js with `NEXT_PUBLIC_API_URL` pointing to the public API. Configure Expo EAS and app identifiers before store builds.

Before production: replace the local integer-ID auth approach with Supabase Auth/UUID identity mapping if Supabase is selected; implement production-grade refresh/revocation, email verification, password reset, rate limiting, audit logs, RLS, observability, backups, and privacy controls. Do not expose database credentials or Gemini keys to clients.
