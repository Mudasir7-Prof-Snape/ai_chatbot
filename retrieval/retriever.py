# from vectorstore.vectordb import VECTOR_DB

# def retrieve_documents(query):

#     retriever = VECTOR_DB.as_retriever(
#         search_type="similarity",
#         search_kwargs={"k": 8}
#     )

#     docs = retriever.invoke(query)

#     # simple reranking
#     docs = sorted(docs, key=lambda x: len(x.page_content), reverse=True)

#     return docs[:5].

from vectorstore.vectordb import get_vector_db

def retrieve_documents(query):

    db = get_vector_db()  

    retriever = db.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 8}
    )

    docs = retriever.invoke(query)

    docs = sorted(docs, key=lambda x: len(x.page_content), reverse=True)

    return docs[:5]