from vectorstore.vectordb import VECTOR_DB

def index_documents(document_chunks):
    VECTOR_DB.add_documents(document_chunks)
    # VECTOR_DB.persist()