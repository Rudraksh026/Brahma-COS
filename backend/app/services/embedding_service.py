import ollama


EMBEDDING_MODEL = "nomic-embed-text"


def generate_embedding(text: str):

    response = ollama.embeddings(
        model=EMBEDDING_MODEL,
        prompt=text
    )

    return response["embedding"]