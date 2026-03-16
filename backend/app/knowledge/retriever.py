from sentence_transformers import SentenceTransformer  # type: ignore
import chromadb  # type: ignore
from app.config.settings import settings

model = SentenceTransformer(
    "all-MiniLM-L6-v2",
    device="cpu",
    token=settings.hf_token
)

client = chromadb.PersistentClient(path="../../storage/vector_db")
collection = client.get_or_create_collection(name="documents")


def retrieve_context(query, k=3):

    query_embedding = model.encode([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    documents = results["documents"][0]

    return documents
