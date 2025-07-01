import requests
from typing import List


def get_gemini_embedding(text: str, api_key: str) -> List[float]:
    """
    Gets the embedding for a given text using Gemini embedding API.

    Args:
        text (str): The text to embed.
        api_key (str): User's Gemini API key.

    Returns:
        List[float]: The embedding vector.
    """
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-exp-03-07:embedContent"
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key,
    }
    body = {
        "model": "gemini-embedding-exp-03-07",
        "content": {"parts": [{"text": text}]},
        "taskType": "SEMANTIC_SIMILARITY",
    }

    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()

    return response.json()["embedding"]
