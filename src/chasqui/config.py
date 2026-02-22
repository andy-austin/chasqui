from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    whatsapp_api_token: str
    whatsapp_phone_number_id: str
    whatsapp_verify_token: str = "chasqui_token_2026"
    whatsapp_api_version: str = "v22.0"

    @property
    def whatsapp_api_base_url(self) -> str:
        return f"https://graph.facebook.com/{self.whatsapp_api_version}"

    model_config = {"env_file": ".env"}


@lru_cache
def _get_settings() -> Settings:
    return Settings()


class _SettingsProxy:
    """Lazy proxy that defers Settings instantiation until first attribute access."""

    def __getattr__(self, name: str):
        return getattr(_get_settings(), name)


settings = _SettingsProxy()
