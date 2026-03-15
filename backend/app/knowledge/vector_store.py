import chromadb  # type: ignore

client = chromadb.Client()

collection = client.get_or_create_collection(name="documents")


def store_embeddings(chunks, embeddings):

    ids = [f"id_{i}" for i in range(len(chunks))]

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids
    )
