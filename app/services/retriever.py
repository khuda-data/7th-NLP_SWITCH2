from app.utils.vector_db import get_vectorstore
from sentence_transformers import SentenceTransformer

embedder = SentenceTransformer("jhgan/ko-sbert-nli")
vs = get_vectorstore()

def retrieve_relevant_docs(query):
    query_vec = embedder.encode(query)
    results = vs.similarity_search_by_vector(query_vec.tolist(), k=3)
    return [r.page_content for r in results]