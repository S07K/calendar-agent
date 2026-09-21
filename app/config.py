from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_key: str
    base_url: str
    model: str

    model_config = {"env_file": ".env"}