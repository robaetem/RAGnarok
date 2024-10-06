from sentence_transformers import SentenceTransformer
from tqdm import tqdm

def get_embedding_client():
    model = SentenceTransformer("nomic-ai/nomic-embed-text-v1", trust_remote_code=True)
    return model

def embed_chunks(chunks):
    """Adds embeddings to chunks
    """
    print("Embedding chunks")
    model = get_embedding_client()
    for chunk in tqdm(chunks):
        chunk["embedding"] = model.encode(chunk["content"])
    return chunks

def embed_string(input: str):
    model = get_embedding_client()
    embedding = model.encode(input)
    return embedding