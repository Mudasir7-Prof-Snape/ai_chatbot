# # #from langchain_community.vectorstores import Chroma
# from langchain_chroma import Chroma
# from config import EMBEDDING_MODEL, VECTOR_DB_DIR

# VECTOR_DB = Chroma(
#     collection_name="pdf_rag",
#     embedding_function=EMBEDDING_MODEL,
#     persist_directory=VECTOR_DB_DIR
# )

from langchain_community.vectorstores import Chroma
from config import EMBEDDING_MODEL, VECTOR_DB_DIR

def get_vector_db():
    return Chroma(
        collection_name="pdf_rag",
        embedding_function=EMBEDDING_MODEL,
        persist_directory=VECTOR_DB_DIR
    )