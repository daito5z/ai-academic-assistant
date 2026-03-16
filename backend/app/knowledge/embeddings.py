from sentence_transformers import SentenceTransformer  # type: ignore

model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(text_chunks, batch_size=32):

    all_embeddings = []

    for i in range(0, len(text_chunks), batch_size):

        batch = text_chunks[i:i + batch_size]

        embeddings = model.encode(
            batch,
            batch_size=batch_size,
            show_progress_bar=False
        )

        all_embeddings.extend(embeddings)

    return all_embeddings
