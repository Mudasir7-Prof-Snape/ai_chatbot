# from vectorstore.vectordb import VECTOR_DB

# def list_documents():

#     data = VECTOR_DB.get()

#     sources = set()

#     for meta in data["metadatas"]:
#         if "source" in meta:
#             sources.add(meta["source"])

#     return list(sources)


# def delete_document(file_name):

#     VECTOR_DB._collection.delete(
#         where={"source": file_name}
#     )

from vectorstore.vectordb import get_vector_db

def list_documents():

    db = get_vector_db()
    data = db.get()

    sources = set()

    for meta in data["metadatas"]:
        if "source" in meta:
            sources.add(meta["source"])

    return list(sources)


def delete_document(file_name):

    db = get_vector_db()

    db._collection.delete(
        where={"source": file_name}
    )