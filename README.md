# PDF Gemini Chat 🤖 💬

PDF Gemini Chat is a Python-based application that enables users to interact with PDF documents using conversational AI. The project leverages document chunking, embedding, and retrieval techniques to provide intelligent responses to user queries about the content of uploaded PDFs.

## Features
- Upload and process PDF documents
- Chunk PDF content for efficient retrieval
- Generate embeddings for semantic search
- Retrieve relevant information from PDFs using conversational queries
- Modular codebase for easy extension and maintenance

## Project Structure
```
requirements.txt
app/
    app.py
utils/
    __init__.py
    chatbot.py
    chunker.py
    embedding.py
    indexer.py
    pdf_utils.py
    retriever.py
```

- `app/app.py`: Main application entry point
- `utils/`: Utility modules for PDF processing, chunking, embedding, indexing, retrieval, and chatbot logic

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/mobley-trent/pdf_gemini_chat.git
   cd pdf_gemini_chat
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the main application:
```bash
streamlit run app/app.py
```

## Requirements
- Python 3.8+
- See `requirements.txt` for Python package dependencies

## License
This project is licensed under the MIT License.
