from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(model_name="jhgan/ko-sbert-nli")

def get_vectorstore():
    return Chroma(persist_directory="data/chroma", embedding_function=embedding)
