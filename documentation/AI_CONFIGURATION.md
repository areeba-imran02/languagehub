# AI configuration

Set `GEMINI_API_KEY`, `GEMINI_PRIMARY_MODEL`, `GEMINI_FALLBACK_MODEL`, and `AI_TIMEOUT_SECONDS` in the backend environment. The adapter uses Google's Gemini REST `generateContent` endpoint and keeps the key server-side. The defaults are configurable and must be checked against Google's current model catalog and project quota before deployment. A missing key produces HTTP 503 with a setup explanation; it never fabricates a tutor answer.

Modes: `fast` tries primary then fallback; `smart` currently shares the same provider path and does not yet include a reviewer pass; `fallback` tries only the fallback model. Exponential retry is bounded. Speech recognition and audio pronunciation scoring are not implemented in this release.
