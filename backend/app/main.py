from fastapi import FastAPI  # type: ignore
from app.api.chat import router as chat_router
from app.api.pdf import router as pdf_router
from app.api.email import router as email_router
from dotenv import load_dotenv

load_dotenv()

print("Starting AI Academic Assistant...")

app = FastAPI(title="AI Academic Assistant")

app.include_router(chat_router)
app.include_router(pdf_router)
app.include_router(email_router)
