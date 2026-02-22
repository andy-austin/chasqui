"""Vercel entrypoint — re-exports the FastAPI app."""

from chasqui.main import app

__all__ = ["app"]
