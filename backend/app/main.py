from fastapi import FastAPI  # type: ignore
from app.api.chat import router as chat_router
from app.api.pdf import router as pdf_router

app = FastAPI(title="AI Academic Assistant")

app.include_router(chat_router)
app.include_router(pdf_router)
