# Coding Conventions & Development Workflow

## Development Commands

```bash
# Install dependencies
uv sync

# Run locally (with hot reload)
uvicorn src.chasqui.main:app --reload --port 8000

# Run with Docker
docker compose up --build

# Run tests
uv run pytest

# Run tests verbose
uv run pytest -v

# Lint
uv run ruff check src/ tests/

# Lint with auto-fix
uv run ruff check --fix src/ tests/

# Expose local server for webhook testing
ngrok http 8000
```

## Code Style

- **Async by default**: Use `async/await` for all I/O-bound operations (HTTP calls to Meta, future DB queries).
- **Type hints**: Required on all function signatures and return types.
- **Pydantic models**: Use for request/response validation and data structures.
- **Thin route handlers**: Route functions handle HTTP concerns only (parse request, return response). Business logic belongs in `services/`.
- **Logging**: Use Python's `logging` module with `logger = logging.getLogger(__name__)`. Prefer structured info (`logger.info("Message sent to %s", phone)`) over f-strings in log calls.
- **Ruff**: Enforced rules — `E` (pycodestyle), `F` (pyflakes), `I` (isort), `N` (naming), `W` (warnings), `UP` (pyupgrade). Line length: 100.

## Project Patterns

### Configuration
Settings are loaded once at module level in `config.py` via `pydantic-settings`. Import the singleton:
```python
from chasqui.config import settings
```
All secrets come from environment variables (`.env` file locally, injected in production).

### Adding a New Route
1. Create a file in `src/chasqui/routes/` with an `APIRouter`.
2. Register it in `src/chasqui/main.py` with `app.include_router(...)`.
3. Add tests in `tests/`.

### Adding a New Service
1. Create a file in `src/chasqui/services/`.
2. Import and use it from route handlers.
3. Keep services focused on a single external integration or domain.

## Testing

- Tests use `httpx.AsyncClient` with `ASGITransport` to hit the FastAPI app directly (no server needed).
- Test env vars are set in `tests/conftest.py` before any app imports.
- `asyncio_mode = "auto"` in pyproject.toml — no need for `@pytest.mark.asyncio` but it's fine to include for clarity.
