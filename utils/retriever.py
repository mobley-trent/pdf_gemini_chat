import faiss
import numpy as np
from typing import List
from utils.embedding import get_gemini_embedding


def retrieve_relevant_chunks(
    query: str,
    faiss_index: faiss.IndexFlatL2,
    chunks: List[str],
    api_key: str,
    top_k: int = 5,
) -> List[str]:
    """
    Finds the top-k relevant chunks given a user query.

    Args:
        query (str): The user's question.
        faiss_index (faiss.Index): The FAISS index of chunk embeddings.
        chunks (List[str]): Original text chunks.
        api_key (str): User's Gemini API key.
        top_k (int): Number of chunks to retrieve.

    Returns:
        List[str]: Top-k most relevant chunks.
    """
    query_embedding = get_gemini_embedding(query, api_key)
    query_vector = np.array([query_embedding["values"]]).astype("float32")

    distances, indices = faiss_index.search(query_vector, top_k)
    return [chunks[i] for i in indices[0] if i < len(chunks)]
