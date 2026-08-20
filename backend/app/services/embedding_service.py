EMBEDDING_MODEL = "nomic-embed-text"

def generate_embedding(text: str):
    try:
        import ollama
        response = ollama.embeddings(model=EMBEDDING_MODEL, prompt=text)
        return response["embedding"]
    except Exception as exc:
        print(f"[KOSH] Embedding unavailable: {exc}")
        return None
