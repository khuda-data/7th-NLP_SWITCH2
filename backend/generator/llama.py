from llama_cpp import Llama
import os
from dotenv import load_dotenv
load_dotenv()

llm = Llama.from_pretrained(
    repo_id="thos0412/llama-2-ko-7b-Q4_K_M-GGUF",
    filename="llama-2-ko-7b-q4_k_m.gguf",
    chat_format="llama-2"
)

def generate_llama_answer(question, retrieved_docs):
    context_text = "\n".join(f"- {doc}" for doc in retrieved_docs)

    full_prompt = f"""당신은 공모전 추천 챗봇입니다.
아래는 사용자 질문과 관련된 공모전 정보들입니다. 반드시 이 중에서 가장 관련 있는 단 하나의 공모전만 선택해 아래 형식으로 요약해서 보여주세요.
관련 정보가 없으면 "해당 주제의 공모전은 현재 확인되지 않습니다."라고만 답변하세요.

[공모전 요약 형식]
제목: ...
주최: ...
기간: ...
요약: ... (2~3문장)

공모전 정보:
{context_text}

사용자 질문: {question}
"""

    response = llm(full_prompt, max_tokens=256, temperature=0.7, stop=["<|end|>"])

    content = response["choices"][0]["text"].strip() if "choices" in response else response.get("text", "").strip()

    # 후처리: 실제 context 제목 중 하나와 일치하지 않으면 환각으로 간주
    titles = [doc.split("|")[0].replace("title:", "").strip() for doc in retrieved_docs]
    hallucinated = True
    for title in titles:
        if title in content:
            hallucinated = False
            break

    if hallucinated or not content:
        return "해당 주제의 공모전은 현재 확인되지 않습니다."

    return content