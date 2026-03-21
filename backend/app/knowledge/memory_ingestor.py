from app.knowledge.chunker import chunk_text
from app.knowledge.embeddings import generate_embeddings
from app.knowledge.vector_store import store_embeddings


def store_interaction(query, response):

    text = f"""
User Question: {query}
Assistant Answer: {response}
"""

    chunks = chunk_text(text)
    embeddings = generate_embeddings(chunks)

    store_embeddings(
        chunks,
        embeddings,
        document_name="memory",
        metadata_extra={"source": "memory"}
    )
