from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")


def chunk_text(text, max_tokens=300):

    tokens = tokenizer.encode(text)
    chunks = []

    for i in range(0, len(tokens), max_tokens):
        chunk = tokenizer.decode(tokens[i:i+max_tokens])
        chunks = [c for c in chunks if c.strip()]
        chunks.append(chunk)

    return chunks
