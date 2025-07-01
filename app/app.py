import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from utils.pdf_utils import extract_text_from_pdf
from utils.chunker import chunk_text
from utils.embedding import get_gemini_embedding
from utils.indexer import build_faiss_index
from utils.retriever import retrieve_relevant_chunks
from utils.chatbot import ask_gemini_with_context

# App title
st.set_page_config(page_title="📄 Chat with your PDF using Gemini", layout="wide")
st.title("📄 Chat with your PDF using Gemini")

# Sidebar: API Key input
with st.sidebar:
    st.header("🔑 Gemini API Setup")
    api_key = st.text_input("Enter your Gemini API Key", type="password")

    if api_key:
        st.session_state["api_key"] = api_key
        st.success("API key set!", icon="✅")

# PDF Upload
uploaded_file = st.file_uploader("Upload your PDF file", type="pdf")

if uploaded_file:
    try:
        st.session_state["uploaded_pdf"] = uploaded_file
        st.success(f"Uploaded: {uploaded_file.name}", icon="📄")

        with st.spinner("📄 Processing PDF..."):
            if "extracted_text" not in st.session_state:
                extracted_text = extract_text_from_pdf(uploaded_file)
                st.session_state["extracted_text"] = extracted_text

            # Chuck text if not already done
            if (
                "extracted_text" in st.session_state
                and "text_chunks" not in st.session_state
            ):
                chunks = chunk_text(extracted_text)
                st.session_state["text_chunks"] = chunks

            # Embed chunks with Gemini
            if (
                "text_chunks" in st.session_state
                and "chunk_embeddings" not in st.session_state
            ):
                embeddings = []
                for chunk in st.session_state["text_chunks"]:
                    if "api_key" not in st.session_state:
                        raise ValueError("API key is required for embedding.")
                    embedding = get_gemini_embedding(chunk, st.session_state["api_key"])
                    embeddings.append(embedding["values"])

                if embeddings:
                    st.session_state["chunk_embeddings"] = embeddings

                    # Build FAISS index
                    index = build_faiss_index(embeddings)
                    st.session_state["faiss_index"] = index

        st.success("✅ Text extracted successfully!")
    except ValueError as ve:
        st.error(f"❌ Error: {ve}")
    except Exception as e:
        st.error(f"❌ Error processing PDF: {e}")

st.divider()

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about the PDF"):
    if "api_key" not in st.session_state:
        st.error("❌ Please provide your Gemini API key in the sidebar.")
    elif "uploaded_pdf" not in st.session_state:
        st.error("❌ Please upload a PDF file first.")
    elif "extracted_text" not in st.session_state:
        st.error("❌ Text has not been extracted yet.")
    elif "faiss_index" not in st.session_state:
        st.error("❌ PDF not indexed yet.")
    else:
        st.chat_message("user").markdown(prompt)

        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.spinner("🔍 Retrieving relevant context..."):
            top_chunks = retrieve_relevant_chunks(
                query=prompt,
                faiss_index=st.session_state["faiss_index"],
                chunks=st.session_state["text_chunks"],
                api_key=st.session_state["api_key"],
            )

        with st.spinner("🤖 Asking Gemini..."):
            response = ask_gemini_with_context(
                question=prompt,
                context_chunks=top_chunks,
                api_key=st.session_state["api_key"],
            )

        with st.chat_message("assistant"):
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})
