# Chasqui - WhatsApp Notifications Microservice

## Project Overview

**Chasqui** is a microservice responsible for managing WhatsApp notifications for the Torke platform. It integrates with the Meta WhatsApp Business Cloud API to send automated messages (vehicle reports, appointment reminders, status updates) to mechanics and workshop clients.

> "Chasqui" — named after the Inca messengers who ran relay routes across the empire to deliver messages. This service does the same: delivers messages fast and reliably.

## Architecture

- **Runtime**: Python 3.12+
- **Framework**: FastAPI (async, high-performance)
- **Package Manager**: UV (fast, modern Python package manager)
- **Containerization**: Docker + docker-compose for local dev
- **API Integration**: Meta WhatsApp Business Cloud API v21.0

## Project Structure

```
chasqui/
├── src/
│   └── chasqui/
│       ├── __init__.py
│       ├── main.py              # FastAPI app entry point
│       ├── config.py            # Settings via pydantic-settings
│       ├── routes/
│       │   ├── __init__.py
│       │   ├── webhook.py       # WhatsApp webhook (GET verify + POST receive)
│       │   └── health.py        # Health check endpoint
│       └── services/
│           ├── __init__.py
│           └── whatsapp.py      # Meta Cloud API client (send messages)
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_webhook.py
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── CLAUDE.md
└── .gitignore
```

## Key Configuration (Environment Variables)

| Variable | Description |
|---|---|
| `WHATSAPP_API_TOKEN` | Meta Cloud API bearer token (temporary: 24h, permanent: System User token) |
| `WHATSAPP_PHONE_NUMBER_ID` | The Phone Number ID assigned by Meta (not the phone number itself) |
| `WHATSAPP_VERIFY_TOKEN` | Secret token for webhook verification handshake |
| `WHATSAPP_API_VERSION` | Meta API version, default `v21.0` |

## Meta WhatsApp Integration Notes

### Phone Number Requirements
- The phone number used for the API **must never have been registered** with WhatsApp or WhatsApp Business apps.
- Buy a fresh prepaid SIM (Antel/Claro/Movistar in Uruguay), keep it in a secondary phone only for SMS verification.
- Meta sends a 6-digit SMS code to verify ownership.

### Webhook Flow
1. **Verification (GET)**: Meta sends a GET request with `hub.mode=subscribe`, `hub.verify_token`, and `hub.challenge`. The server must validate the token and return the challenge value as plain text.
2. **Incoming Messages (POST)**: Meta sends a POST with message payloads when users reply. Subscribe to the `messages` field in webhook configuration.

### API Limits (Unverified Business)
- **250 business-initiated conversations per 24h** (sufficient for testing and early production).
- To increase limits, complete Meta Business Verification (requires fiscal documents).

### Message Types
- **Template messages**: Pre-approved messages that can initiate conversations (require Meta approval).
- **Free-form messages**: Text, media, documents — only within a 24h conversation window after user interaction.

## Development Commands

```bash
# Install dependencies
uv sync

# Run locally
uvicorn src.chasqui.main:app --reload --port 8000

# Run with Docker
docker compose up --build

# Run tests
uv run pytest

# Expose local server (for webhook testing)
ngrok http 8000
```

## Coding Conventions

- Use `async/await` for all I/O-bound operations (HTTP calls to Meta API).
- Type hints on all function signatures.
- Pydantic models for request/response validation.
- Settings loaded via `pydantic-settings` from environment variables.
- Keep route handlers thin — business logic lives in `services/`.
- Logging via Python's `logging` module with structured context.
