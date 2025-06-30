# generator/generator.py
import openai
import os
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_answer(question, retrieved_docs):
    context = "\n\n".join(retrieved_docs)
    prompt = f"""당신은 공모전 전문 챗봇입니다. 아래 조건을 반드시 지켜주세요.

1. 아래 정보에 없는 공모전을 임의로 만들어내지 마세요.
2. 관련 정보가 없으면 "해당 주제의 공모전은 현재 확인되지 않습니다."라고만 답변하세요.
3. 관련 정보가 존재하면 요약하여 자연스럽게 전달하세요.

사용자 질문:
"{question}"

아래는 관련 공모전 정보입니다:
{context}
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message["content"]