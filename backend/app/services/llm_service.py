from app.knowledge.retriever import retrieve_context
import requests  # type: ignore
from app.config.settings import settings


class LLMService:

    @staticmethod
    def generate_response(prompt: str):

        context_chunks = retrieve_context(prompt)

        context = "\n\n".join(
            [f"Chunk {i+1}: {chunk}" for i, chunk in enumerate(context_chunks)]
        )

        final_prompt = f"""
        You are an academic assistant.

        Answer the question ONLY using the provided context.
        If the answer is not in the context, say:
        "I could not find the answer in the document."
        Use the context below to answer the question.

Context:
{context}

Question:
{prompt}
"""

        response = requests.post(
            f"{settings.ollama_url}/api/generate",
            json={
                "model": settings.model_name,
                "prompt": final_prompt,
                "stream": False
            }
        )

        return response.json()["response"]
