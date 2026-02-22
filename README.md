# Chasqui

WhatsApp notifications microservice for the [Torke](https://torke.com) platform. Sends and receives WhatsApp messages via the Meta WhatsApp Business Cloud API to notify mechanics and workshops about vehicle reports, appointment reminders, and status updates.

> *"Chasqui"* — named after the Inca messengers who ran relay routes across the empire to deliver messages.

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12+ |
| Framework | FastAPI (async) |
| HTTP Client | httpx (async) |
| Config | pydantic-settings |
| Package Manager | UV |
| Containerization | Docker |
| External API | Meta WhatsApp Business Cloud API v21.0 |
| Testing | pytest + pytest-asyncio |
| Linting | Ruff |

## Getting Started

### Prerequisites

- Python 3.12+
- [UV](https://docs.astral.sh/uv/) package manager
- Docker (optional, for containerized runs)

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd chasqui

# Install dependencies
uv sync

# Install dev dependencies (tests, linting)
uv sync --dev
```

### Configuration

Copy the example environment file and fill in your Meta API credentials:

```bash
cp .env.example .env
```

| Variable | Required | Description |
|---|---|---|
| `WHATSAPP_API_TOKEN` | Yes | Meta Cloud API bearer token |
| `WHATSAPP_PHONE_NUMBER_ID` | Yes | Phone Number ID assigned by Meta |
| `WHATSAPP_VERIFY_TOKEN` | Yes | Secret token for webhook verification handshake |
| `WHATSAPP_API_VERSION` | No | Meta API version (default: `v21.0`) |

For detailed WhatsApp setup instructions (phone number registration, Meta Business Manager configuration, webhook setup), see [`.ai/WHATSAPP_INTEGRATION.md`](.ai/WHATSAPP_INTEGRATION.md).

### Running Locally

```bash
uvicorn src.chasqui.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.

### Running with Docker

```bash
docker compose up --build
```

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Health check — returns `{"status": "ok"}` |
| GET | `/webhook/whatsapp` | Meta webhook verification (challenge-response) |
| POST | `/webhook/whatsapp` | Receive incoming WhatsApp messages and status updates |

## Project Structure

```
chasqui/
├── src/chasqui/
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Settings via pydantic-settings
│   ├── routes/
│   │   ├── health.py        # GET /health
│   │   └── webhook.py       # Webhook verify + receive
│   └── services/
│       └── whatsapp.py      # WhatsAppClient — sends messages via Meta API
├── tests/
│   ├── conftest.py          # Shared fixtures
│   └── test_webhook.py      # Endpoint tests
├── .ai/                     # Documentation for AI agents
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
└── .env.example
```

## Testing

```bash
# Run tests
uv run pytest -v

# Lint
uv run ruff check src/ tests/

# Lint with auto-fix
uv run ruff check --fix src/ tests/
```

## WhatsApp Client Usage

The `WhatsAppClient` supports three message types:

```python
from chasqui.services.whatsapp import WhatsAppClient

client = WhatsAppClient()

# Plain text (requires active 24h conversation window)
await client.send_text_message("59899123456", "Your vehicle is ready!")

# Template message (can initiate conversations)
await client.send_template_message("59899123456", "appointment_reminder")

# Document (e.g. PDF report, requires active conversation window)
await client.send_document_message(
    "59899123456",
    document_url="https://example.com/report.pdf",
    filename="vehicle_report.pdf",
    caption="Here is your vehicle report",
)
```

## License

Private — Torke platform internal service.
