import chromadb  # type: ignore
from chromadb.config import Settings
import uuid
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

DB_PATH = os.path.join(BASE_DIR, "storage", "vector_db")

client = chromadb.PersistentClient(path=DB_PATH)

collection = client.get_or_create_collection(name="documents")


def document_exists(message_id):

    results = collection.get(
        where={"message_id": message_id}
    )

    return len(results["ids"]) > 0


def store_embeddings(chunks, embeddings, document_name, metadata_extra=None):

    metadatas = []

    for _ in chunks:
        meta = {
            "document": document_name,
            "source": metadata_extra.get("source", "unknown")
        }

        meta.update(metadata_extra or {})
        metadatas.append(meta)

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=[str(uuid.uuid4()) for _ in chunks],
        metadatas=metadatas
    )
