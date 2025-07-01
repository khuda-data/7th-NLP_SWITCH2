# pipeline/rag_pipeline.py
from retriever.retriever import retrieve
from generator.llama import generate_llama_answer
from generator.llama import llm  # llm 객체를 직접 사용

def llama_pipeline(user_question):
    related_docs = retrieve(user_question)

    def select_top_docs_by_token_limit(docs, max_tokens=400):
        selected = []
        total = 0
        for text in docs:  # ✅ 문자열 바로 사용
            token_len = len(llm.tokenize(text.encode("utf-8")))
            if total + token_len > max_tokens:
                break
            selected.append(text)
            total += token_len
        return selected

    selected_context = select_top_docs_by_token_limit(related_docs)
    print("🔍 Selected context:\n", selected_context)

    if not selected_context:
        return "해당 주제의 공모전은 현재 확인되지 않습니다."

    answer = generate_llama_answer(user_question, selected_context)
    print("💬 Generated answer:\n", answer)
    return answer