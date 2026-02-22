# Project Context

## What is Chasqui?

**Chasqui** is a microservice responsible for managing WhatsApp notifications for the **Torke** platform. It integrates with the Meta WhatsApp Business Cloud API to send automated messages (vehicle reports, appointment reminders, status updates) to mechanics and workshop clients in Uruguay.

> "Chasqui" — named after the Inca messengers who ran relay routes across the empire to deliver messages.

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12+ |
| Framework | FastAPI (async) |
| HTTP client | httpx (async) |
| Config | pydantic-settings (loads from `.env`) |
| Package manager | UV |
| Containerization | Docker + docker-compose |
| External API | Meta WhatsApp Business Cloud API v21.0 |
| Testing | pytest + pytest-asyncio |
| Linting | ruff |

## Directory Layout

```
chasqui/
├── .ai/                         # AI agent context (you are here)
├── src/
│   └── chasqui/
│       ├── __init__.py
│       ├── main.py              # FastAPI app entry point, router registration
│       ├── config.py            # Settings singleton via pydantic-settings
│       ├── routes/
│       │   ├── __init__.py
│       │   ├── webhook.py       # GET /webhook/whatsapp (verify) + POST (receive)
│       │   └── health.py        # GET /health
│       └── services/
│           ├── __init__.py
│           └── whatsapp.py      # WhatsAppClient — sends messages via Meta API
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Shared fixtures (async test client)
│   └── test_webhook.py          # Webhook + health endpoint tests
├── pyproject.toml               # Project metadata, deps, tool config
├── uv.lock                      # Locked dependency versions
├── Dockerfile
├── docker-compose.yml
├── .env.example                 # Template for required environment variables
├── CLAUDE.md                    # Quick-reference for Claude Code specifically
└── .gitignore
```

## Key Environment Variables

| Variable | Required | Description |
|---|---|---|
| `WHATSAPP_API_TOKEN` | Yes | Meta Cloud API bearer token |
| `WHATSAPP_PHONE_NUMBER_ID` | Yes | Phone Number ID assigned by Meta (not the phone number itself) |
| `WHATSAPP_VERIFY_TOKEN` | Yes | Secret token for webhook verification handshake |
| `WHATSAPP_API_VERSION` | No | Meta API version, defaults to `v21.0` |

## API Endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Health check, returns `{"status": "ok"}` |
| GET | `/webhook/whatsapp` | Meta webhook verification (challenge-response) |
| POST | `/webhook/whatsapp` | Receive incoming WhatsApp messages/status updates |
