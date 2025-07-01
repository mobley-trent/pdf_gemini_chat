import faiss
import numpy as np
from typing import List


def build_faiss_index(embeddings: List[List[float]]) -> faiss.IndexFlatL2:
    """
    Builds a FAISS index from a list of embeddings.

    Args:
        embeddings (List[List[float]]): Embedding vectors.

    Returns:
        faiss.IndexFlatL2: The FAISS index.
    """
    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype("float32"))
    return index
