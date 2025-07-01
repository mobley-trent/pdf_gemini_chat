from PyPDF2 import PdfReader
from typing import IO


def extract_text_from_pdf(file: IO) -> str:
    """
    Extracts and returns all text from a PDF file-like object.

    Args:
        file (IO): A file-like object, typically from Streamlit's file uploader.

    Returns:
        str: The extracted text.
    """
    reader = PdfReader(file)
    full_text = []

    for page_num, page in enumerate(reader.pages):
        try:
            text = page.extract_text()
            if text:
                full_text.append(text)
        except Exception as e:
            print(f"Error reading page {page_num}: {e}")

    return "\n\n".join(full_text)
