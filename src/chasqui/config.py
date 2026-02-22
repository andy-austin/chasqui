from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    whatsapp_api_token: str
    whatsapp_phone_number_id: str
    whatsapp_verify_token: str = "torke_super_secret_token_2026"
    whatsapp_api_version: str = "v21.0"

    @property
    def whatsapp_api_base_url(self) -> str:
        return f"https://graph.facebook.com/{self.whatsapp_api_version}"

    model_config = {"env_file": ".env"}


settings = Settings()
