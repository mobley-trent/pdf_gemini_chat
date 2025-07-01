from typing import List


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
    """
    Splits text into overlapping chunks.

    Args:
        text (str): The full raw text to chunk.
        chunk_size (int): Number of words per chunk.
        overlap (int): Number of words to overlap between chunks.

    Returns:
        List[str]: A list of text chunks.
    """
    words = text.split()
    chunks = []

    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap  # Slide forward with overlap

    return chunks
