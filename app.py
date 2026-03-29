import streamlit as st

from ingestion.loader import save_uploaded_file, load_pdf_documents
from ingestion.chunker import chunk_documents
from ingestion.indexer import index_documents
from agent.memory import get_chat_history, update_chat_history

from agent.pipeline import agentic_rag_pipeline

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.write(chat["user"])

    with st.chat_message("assistant"):
        st.write(chat["assistant"])

# UI
st.title("JILE guide AI")

uploaded_pdfs = st.file_uploader(
    "Upload PDFs",
    type="pdf",
    accept_multiple_files=True
)

# Process PDFs
if uploaded_pdfs and "docs_loaded" not in st.session_state:

    for pdf in uploaded_pdfs:
        path = save_uploaded_file(pdf)
        raw_docs = load_pdf_documents(path)
        chunks = chunk_documents(raw_docs)
        index_documents(chunks)

    st.session_state.docs_loaded = True
    st.success("Documents processed!")

# Chat
user_input = st.chat_input("Ask your question...")

if user_input:

    with st.chat_message("user"):
        st.write(user_input)

    with st.spinner("Thinking..."):

        chat_history = get_chat_history(st.session_state)

        response = agentic_rag_pipeline(user_input, chat_history)

    with st.chat_message("assistant"):
        st.write(response)

    # Save memory
    update_chat_history(st.session_state, user_input, response)