from fastapi import FastAPI  # type: ignore
from app.api.chat import router as chat_router

app = FastAPI(title="AI Academic Assistant")

app.include_router(chat_router)
