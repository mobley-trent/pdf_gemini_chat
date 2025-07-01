import requests
from typing import List


def ask_gemini_with_context(
    question: str,
    context_chunks: List[str],
    api_key: str,
) -> str:
    """
    Uses Gemini 2.5 to answer a question using context chunks.

    Args:
        question (str): The user's query.
        context_chunks (List[str]): Relevant chunks from the PDF.
        api_key (str): User's Gemini API key.

    Returns:
        str: Gemini's response.
    """
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

    headers = {"Content-Type": "application/json", "x-goog-api-key": api_key}

    # Prepare the prompt
    context_text = "\n\n".join(context_chunks)
    system_prompt = (
        "You are a helpful assistant. Use the provided context to answer the question.\n\n"
        f"Context:\n{context_text}\n\n"
        f"Question: {question}"
    )

    payload = {"contents": [{"parts": [{"text": system_prompt}]}]}

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    candidates = response.json().get("candidates", [])
    if candidates:
        return candidates[0]["content"]["parts"][0]["text"]
    else:
        return "No answer returned by the model."
