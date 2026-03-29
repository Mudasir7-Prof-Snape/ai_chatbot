import os
from langchain_ollama import OllamaEmbeddings
from langchain_ollama.llms import OllamaLLM

PDF_STORAGE_PATH = "data/pdfs/"
VECTOR_DB_DIR = "vector_db"

os.makedirs(PDF_STORAGE_PATH, exist_ok=True)

EMBEDDING_MODEL = OllamaEmbeddings(
    model="nomic-embed-text"
)

LANGUAGE_MODEL = OllamaLLM(
    model="qwen2.5:3b"
)