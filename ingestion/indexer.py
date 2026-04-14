# from vectorstore.vectordb import VECTOR_DB

# def index_documents(document_chunks):
#     VECTOR_DB.add_documents(document_chunks)
#     # VECTOR_DB.persist()

from vectorstore.vectordb import get_vector_db

def index_documents(document_chunks):

    db = get_vector_db()
    db.add_documents(document_chunks)