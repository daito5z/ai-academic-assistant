from pydantic_settings import BaseSettings  # type: ignore
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    groq_api_key: str
    model_name: str
    hf_token: str

    class Config:
        env_file = ".env"


settings = Settings()
