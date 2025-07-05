from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

embedding = HuggingFaceEmbeddings(model_name="jhgan/ko-sbert-nli")

def get_vectorstore():
    return Chroma(persist_directory="data/chroma", embedding_function=embedding)
