import requests  # type: ignore
from app.config.settings import settings


class LLMService:

    @staticmethod
    def generate_response(prompt: str):

        response = requests.post(
            f"{settings.ollama_url}/api/generate",
            json={
                "model": settings.model_name,
                "prompt": prompt,
                "stream": False
            }
        )

        data = response.json()

        return data["response"]
