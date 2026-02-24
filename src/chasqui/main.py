import logging

from fastapi import FastAPI

from chasqui.routes import auth, health, home, messages, webhook

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
)

app = FastAPI(
    title="Chasqui",
    description="WhatsApp notifications microservice for Torke",
    version="0.1.0",
)

app.include_router(home.router)
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(webhook.router)
app.include_router(messages.router)
