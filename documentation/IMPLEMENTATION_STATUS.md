# LanguageHub implementation status

Last updated: 2026-11-04. Status reflects source files and checks actually performed in this workspace.

| Area | Status | Evidence / remaining work |
|---|---|---|
| Monorepo and brand system | Implemented | Web, mobile, backend, AI engine, shared, curriculum, infrastructure, docs and tests present; specified palette and tagline in web styling/landing page. |
| Backend API foundation | Implemented and tested | FastAPI v1 routes, SQLAlchemy, auth, vocabulary, progress, courses, learning catalog, grammar and reading answer checks. |
| Authentication | Partial | Register/login/me and password hashing/JWT work; password reset, email verification, refresh/revocation and production identity provider not implemented. |
| Database and migrations | Partial | SQLAlchemy metadata and Alembic initial schema; PostgreSQL driver and settings-based Alembic URL are included; production migration execution still needs deployment validation. |
| Gemini integration | Implemented, awaiting credentials | Server-side HTTP adapter, configurable primary/fallback IDs, bounded retry and explicit missing-key behavior. Live external call not tested. |
| Agent system | Partial | Nine focused agent prompt builders and tutor dispatcher; no production LangGraph workflow, persistent agent state or model-backed reviewer orchestration. |
| Web app | Partial | Landing, login, signup, dashboard, tutor, vocabulary, grammar, reading, writing and conversation screens. Remaining pages, complete auth lifecycle, themes, admin, and end-to-end workflows pending. |
| Mobile app | Starter implemented | Expo app config, navigation shell and initial screen; full module coverage, device testing and native speech workflows pending. |
| Learning modules | Partial | Vocabulary CRUD and progress persistence; curriculum-backed grammar and reading checks; spaced repetition scheduling, assessments, listening audio, speech transcription, and writing history pending. |
| Admin | Partial | Role-protected overview API only; user/course/curriculum/model configuration CRUD and admin UI pending. |
| Supabase RLS | Not production-ready | SQL policy starter exists; policies must be reconciled with selected auth identity and verified against a real Supabase project. |
| Documentation | Partial/usable | Setup, API, database, AI, mobile, deployment, testing, security and implementation status docs exist; revise as implementation expands. |
| Automated backend tests | Passed | `PYTHONPATH=backend pytest -q tests`: 10 passed, no warnings after lifecycle/timezone cleanup. |
| Web build/typecheck | Not verified | npm dependency installation timed out in this environment; no successful Next.js production build or TypeScript check claimed. GitHub Actions is configured to run both. |
| Mobile build/device tests | Not verified | Expo dependency installation, typecheck, emulator, device or signed Android/iOS build are not verified locally. GitHub Actions runs the mobile TypeScript check. |
| Final ZIP | Rebuilt after checks | Source archive excludes secrets, dependencies, caches, generated DBs and build outputs; integrity verified separately. |

## Remaining before production completion

1. Finish the complete course/unit/lesson/exercise/assessment and spaced-repetition data model and workflows.
2. Implement all remaining web and mobile screens and connect every workflow to persisted APIs.
3. Complete specialized AI workflows, model review, usage accounting, rate limiting and live provider tests.
4. Implement secure production authentication, password reset, role management and tested RLS.
5. Complete admin CRUD, notifications and subscription architecture.
6. Implement and test audio assets, microphone permissions, speech-to-text and pronunciation only with real supported providers.
7. Run web production build, mobile typecheck/build and full integration tests in an environment with dependencies and credentials.
8. Configure deployment services and validate migrations against PostgreSQL.

Do not describe the current archive as a complete production-ready product. It is a more capable source foundation with tested backend learning endpoints, but still needs the work above.


## Additional verification hardening (2026-11-04)

- Backend tests now cover curriculum answer-key hiding, progress validation, and per-user progress summaries.
- API catalog responses no longer include correct answer indexes before an answer is submitted.
- FastAPI startup uses a lifespan handler; automatic table creation is restricted to development. Production must run Alembic migrations as a release step.
- Production configuration rejects the known development signing secret and secrets shorter than 32 characters.
- GitHub Actions now runs backend tests, web typecheck + production build, and mobile TypeScript checks. Those Node jobs still need to execute on GitHub because npm dependency installation timed out in this environment.
