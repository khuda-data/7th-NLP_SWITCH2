# pipeline/rag_pipeline.py
from retriever.retriever import retrieve
from generator.generator import generate_answer # 지피티 응답
# from generator.llama import generate_llama_answer # Llama 응답
def rag_pipeline(user_question):
    related_docs = retrieve(user_question)
    answer = generate_answer(user_question, related_docs)
    return answer