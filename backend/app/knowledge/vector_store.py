import chromadb  # type: ignore
from chromadb.config import Settings
import uuid

client = chromadb.PersistentClient(path="../../storage/vector_db")

collection = client.get_or_create_collection(name="documents")


def store_embeddings(chunks, embeddings, document_name):

    ids = [str(uuid.uuid4()) for _ in chunks]

    metadata = [
        {"document": document_name}
        for _ in chunks
    ]

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids,
        metadatas=metadata
    )
