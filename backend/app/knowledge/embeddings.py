from sentence_transformers import SentenceTransformer  # type: ignore

model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(text_chunks):

    embeddings = model.encode(
        text_chunks,
        batch_size=16,
        show_progress_bar=True
    )

    return embeddings
