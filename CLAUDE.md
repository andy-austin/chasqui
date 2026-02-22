# Chasqui — WhatsApp Notifications Microservice

> For full context, see the `.ai/` directory. This file is a quick-reference for Claude Code.

## Quick Facts

- **What**: FastAPI microservice that sends/receives WhatsApp messages via Meta Cloud API
- **Who for**: Torke platform — notifies mechanics and workshops (vehicle reports, reminders)
- **Stack**: Python 3.12, FastAPI, httpx, pydantic-settings, UV, Docker
- **External API**: Meta WhatsApp Business Cloud API v21.0

## Commands

```bash
uv sync                                                  # install deps
uvicorn src.chasqui.main:app --reload --port 8000       # run locally
uv run pytest -v                                         # tests
uv run ruff check src/ tests/                            # lint
docker compose up --build                                # run via docker
```

## Conventions

- Async everywhere (httpx, FastAPI).
- Type hints on all signatures.
- Thin routes, logic in `services/`.
- Config via `pydantic-settings` singleton (`from chasqui.config import settings`).
- Ruff: line-length 100, rules E/F/I/N/W/UP.

## Deeper Context

| Topic | File |
|---|---|
| Architecture & directory layout | `.ai/CONTEXT.md` |
| Code style & dev workflow | `.ai/CONVENTIONS.md` |
| Meta WhatsApp setup & API details | `.ai/WHATSAPP_INTEGRATION.md` |
| Change history | `.ai/CHANGELOG.md` |
