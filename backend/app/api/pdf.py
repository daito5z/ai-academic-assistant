from fastapi import APIRouter, UploadFile  # type: ignore
import tempfile

from app.knowledge.pdf_loader import load_pdf
from app.knowledge.chunker import chunk_text
from app.knowledge.embeddings import generate_embeddings
from app.knowledge.vector_store import store_embeddings

router = APIRouter()


@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile):

    with tempfile.NamedTemporaryFile(delete=False) as temp:

        temp.write(await file.read())

        file_path = temp.name

    text = load_pdf(file_path)

    chunks = chunk_text(text)

    embeddings = generate_embeddings(chunks)

    store_embeddings(chunks, embeddings)

    return {"message": "PDF processed successfully"}
