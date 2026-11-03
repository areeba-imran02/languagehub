# Security

Passwords use salted scrypt hashing; API access tokens are signed HS256 JWTs with expiry. API keys are backend-only. Private vocabulary and progress queries are scoped to the authenticated user; admin overview checks the admin role. This is a development baseline, not a production security certification. Add refresh-token rotation/revocation, email verification, password reset, login throttling, request-level rate limiting, security headers, RLS, audit logging, secret rotation, and a security review before launch. Change the default secret immediately.
