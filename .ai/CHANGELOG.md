# Changelog

All notable changes to this project are documented here, in reverse chronological order.

## 2026-02-23 — Secure API Authentication

### Added
- **JWT authentication** for `/messages/*` endpoints using PyJWT (HS256).
  - Tokens require `sub` (client ID) and `exp` (expiration) claims — no indefinite tokens.
  - `JWT_SECRET` env var configures the signing secret; `JWT_ALGORITHM` defaults to HS256.
- **Token generation script** (`scripts/generate_token.py`) to issue per-client tokens.
- Auth rejection tests: missing token, invalid token, wrong secret, expired token.

### Changed
- Webhook endpoints (`/webhook/whatsapp`) hidden from Swagger docs (`include_in_schema=False`) — they cannot use our auth since Meta calls them directly.
- `/health` remains public (standard for monitoring/load balancers).

## 2026-02-22 — Project Foundation

### Added
- FastAPI microservice scaffold with `src/` layout and UV package management.
- **Webhook endpoints**: `GET /webhook/whatsapp` (Meta verification handshake) and `POST /webhook/whatsapp` (receive incoming messages).
- **Health endpoint**: `GET /health`.
- **WhatsAppClient** service with three send methods:
  - `send_text_message` — plain text within a conversation window.
  - `send_template_message` — pre-approved templates that can initiate conversations.
  - `send_document_message` — PDF/document delivery via URL.
- Configuration via `pydantic-settings` loading from `.env`.
- Dockerfile and docker-compose.yml for local development.
- Test suite: 4 tests covering health, webhook verification (success + failure), and message receipt.
- `.ai/` context directory with project docs for AI agents.
- `CLAUDE.md` quick-reference for Claude Code.
