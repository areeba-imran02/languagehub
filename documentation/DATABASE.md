# Database

SQLAlchemy models currently cover users, profiles, saved words, learning progress, conversations, messages, courses, lessons, and achievements. SQLite is the local default; configure PostgreSQL with `DATABASE_URL=postgresql+psycopg://...` and install a compatible PostgreSQL driver before deployment. Alembic configuration and an initial metadata migration are included.

The current schema is a foundation, not the full requested production schema. Add assessment, exercise, question, answer, review schedule, writing submission, speaking session, role/permission, notification, subscription, and AI usage audit tables before production.
