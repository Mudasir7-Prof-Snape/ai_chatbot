import streamlit as st
import time
from ingestion.loader import save_uploaded_file, load_pdf_documents
from ingestion.chunker import chunk_documents
from ingestion.indexer import index_documents
from agent.memory import get_chat_history, update_chat_history
from agent.pipeline import agentic_rag_pipeline
from vectorstore.db_manager import list_documents, delete_document


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
    padding-bottom: 60px;
}
            
/* Fixed disclaimer at bottom */
.fixed-disclaimer {
    position: fixed;
    bottom: 8px;
    left: 0;
    width: 100%;
    text-align: center;
    font-size: 14px;
    color: white;
    background-color: #0e1117;
    padding: 6px 0;
    z-index: 999;
    border-top: 1px solid #1f2937;
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
    # st.markdown("---")

    st.subheader("📂 Upload Documents")
    uploaded_pdfs = st.file_uploader(
        "Upload PDFs",
        type="pdf",
        accept_multiple_files=True
    )

    # if "docs_loaded" in st.session_state:
    #     container = st.empty()
    #     container.success("Documents Ready")
    #     time.sleep(3)
    #     container.empty()
        
    # else:
    #     st.info("Upload PDFs to begin")

    st.markdown("---")

    if st.button("🧹 Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()
    # --------------------------------------------------------
    st.subheader("📂 Processed Documents")

    docs = list_documents()

    if docs:
        for doc in docs:
            col1, col2 = st.columns([4, 1])

            with col1:
                st.write(doc)

            with col2:
                if st.button("❌", key=doc):
                    delete_document(doc)
                    if "chat_history" in st.session_state:
                        st.session_state.chat_history = []
                    st.success(f"{doc} deleted!")
                    st.rerun()
    else:
        st.info("No documents processed yet.")
# --------------------------------------------------------



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
# if "processed_files" not in st.session_state:
#     st.session_state.processed_files = set()

# if uploaded_pdfs:

#     new_files = []

#     for pdf in uploaded_pdfs:
#         if pdf.name not in st.session_state.processed_files:
#             new_files.append(pdf)

#     if new_files:

#         for pdf in new_files:
#             path = save_uploaded_file(pdf)
#             raw_docs = load_pdf_documents(path)
#             chunks = chunk_documents(raw_docs, pdf.name)
#             index_documents(chunks)

#             # mark as processed
#             st.session_state.processed_files.add(pdf.name)

#         st.success(f"{len(new_files)} new document(s) processed!")

#     # else:
#     #     st.info("These files are already processed.")

if uploaded_pdfs:

    if "processed_files" not in st.session_state:
        st.session_state.processed_files = set()

    new_files_processed = False

    for uploaded_pdf in uploaded_pdfs:

        if uploaded_pdf.name not in st.session_state.processed_files:

            saved_path = save_uploaded_file(uploaded_pdf)

            raw_docs = load_pdf_documents(saved_path)

            chunks = chunk_documents(raw_docs, uploaded_pdf.name)

            index_documents(chunks)

            st.session_state.processed_files.add(uploaded_pdf.name)
            new_files_processed = True

    if new_files_processed:
        st.session_state.docs_loaded = True
        st.success("Documents processed!")
        st.rerun()



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

st.markdown(
    """
    <div class="fixed-disclaimer">
        ⚠️ <b>Disclaimer:</b> AI-generated responses may contain errors. Please verify important information.
    </div>
    """,
    unsafe_allow_html=True
)
