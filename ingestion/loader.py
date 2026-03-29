import os
from langchain_community.document_loaders import PDFPlumberLoader
from config import PDF_STORAGE_PATH

def save_uploaded_file(uploaded_file):
    file_path = os.path.join(PDF_STORAGE_PATH, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path


def load_pdf_documents(file_path):
    loader = PDFPlumberLoader(file_path)
    return loader.load()