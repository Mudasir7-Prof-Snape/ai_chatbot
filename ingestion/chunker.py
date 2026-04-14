# from langchain_text_splitters import RecursiveCharacterTextSplitter

# def chunk_documents(raw_documents):

#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=800,
#         chunk_overlap=150
#     )

#     docs = splitter.split_documents(raw_documents)

#     for i, doc in enumerate(docs):
#         doc.metadata["chunk_id"] = i

#     return docs
from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_documents(raw_documents, file_name):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    docs = splitter.split_documents(raw_documents)

    for i, doc in enumerate(docs):
        doc.metadata["chunk_id"] = i
        doc.metadata["source"] = file_name   

    return docs