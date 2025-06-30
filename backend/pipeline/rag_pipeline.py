# pipeline/rag_pipeline.py
from retriever.retriever import retrieve
from generator.generator import generate_answer

def rag_pipeline(user_question):
    related_docs = retrieve(user_question)
    answer = generate_answer(user_question, related_docs)
    return answer