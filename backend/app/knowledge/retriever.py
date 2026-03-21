from sentence_transformers import SentenceTransformer  # type: ignore
import chromadb  # type: ignore
from app.config.settings import settings
from app.services.query_classifier import classify_query
import os

model = SentenceTransformer(
    "all-MiniLM-L6-v2",
    device="cpu",
    token=settings.hf_token
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

DB_PATH = os.path.join(BASE_DIR, "storage", "vector_db")

client = chromadb.PersistentClient(path=DB_PATH)
print("Hello from retriever.py")
print(client.list_collections())

collection = client.get_or_create_collection(name="documents")


def retrieve_context(query, k=6):

    source = classify_query(query)

    expanded_query = f"""
        User question: {query}

        Rewrite this as a detailed academic query for better search:
        """

    query_embedding = model.encode([expanded_query])[0]

    where_filter = None

    if source != "all":
        where_filter = {"source": source}

    results = collection.get(
        where={"source": "gmail"},
        limit=5
    )

    print(results)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        where=where_filter
    )

    documents = results["documents"][0]

    return documents
