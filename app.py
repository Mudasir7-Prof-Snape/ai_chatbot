import streamlit as st

from ingestion.loader import save_uploaded_file, load_pdf_documents
from ingestion.chunker import chunk_documents
from ingestion.indexer import index_documents
from agent.memory import get_chat_history, update_chat_history
from agent.pipeline import agentic_rag_pipeline


# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="JILE AI Assistant",
    page_icon="",
    layout="wide"
)

# -------------------- CUSTOM CSS --------------------
st.markdown("""
<style>
/* Background */
.main {
    background-color: #0e1117;
    color: white;
}

/* Chat bubbles */
[data-testid="stChatMessage"] {
    border-radius: 12px;
    padding: 10px;
    margin-bottom: 10px;
}

/* User message */
[data-testid="stChatMessage"][aria-label="user"] {
    background-color: #1f2937;
}

/* Assistant message */
[data-testid="stChatMessage"][aria-label="assistant"] {
    background-color: #111827;
}

/* Buttons */
.stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 8px;
    height: 3em;
    width: 100%;
    font-size: 16px;
}

/* File uploader */
.stFileUploader {
    border: 2px dashed #4CAF50;
    padding: 10px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)


# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.title("JILE AI")
    st.markdown("---")

    st.subheader("📂 Upload Documents")
    uploaded_pdfs = st.file_uploader(
        "Upload PDFs",
        type="pdf",
        accept_multiple_files=True
    )

    if "docs_loaded" in st.session_state:
        st.success("Documents Ready")
    # else:
    #     st.info("Upload PDFs to begin")

    st.markdown("---")

    if st.button("🧹 Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()


# -------------------- HEADER --------------------
st.markdown("## JILE AI Assistant")
st.caption("Smart AI powered document assistant")


# -------------------- CHAT HISTORY INIT --------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# -------------------- DISPLAY CHAT --------------------
for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.write(chat["user"])

    with st.chat_message("assistant"):
        st.write(chat["assistant"])


# -------------------- PROCESS PDFs --------------------
if "processed_files" not in st.session_state:
    st.session_state.processed_files = set()

if uploaded_pdfs:

    new_files = []

    for pdf in uploaded_pdfs:
        if pdf.name not in st.session_state.processed_files:
            new_files.append(pdf)

    if new_files:

        for pdf in new_files:
            path = save_uploaded_file(pdf)
            raw_docs = load_pdf_documents(path)
            chunks = chunk_documents(raw_docs)
            index_documents(chunks)

            # mark as processed
            st.session_state.processed_files.add(pdf.name)

        st.success(f"{len(new_files)} new document(s) processed!")

    # else:
    #     st.info("These files are already processed.")



# -------------------- CHAT INPUT --------------------
user_input = st.chat_input("Ask something about your documents...")

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
