from sentence_transformers import SentenceTransformer  # type: ignore
import chromadb  # type: ignore

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.Client()
collection = client.get_or_create_collection(name="documents")


def retrieve_context(query, k=3):

    query_embedding = model.encode([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    return results["documents"][0]
