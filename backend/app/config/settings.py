from pydantic_settings import BaseSettings  # type: ignore


class Settings(BaseSettings):
    ollama_url: str
    model_name: str

    class Config:
        env_file = ".env"


settings = Settings()
