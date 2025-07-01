# generator/generator.py
import openai
import os
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_answer(question, retrieved_docs):
    context = "\n\n".join(retrieved_docs)
    prompt = f"""당신은 공모전 전문 챗봇입니다. 사용자의 질문은 다음과 같습니다:

"{question}"

아래는 관련 공모전 정보입니다:
{context}

이 정보를 바탕으로, 사용자 질문에 직접 답변할 뿐 아니라, 공모전의 핵심 요약 정보(주최, 일정, 시상 내용 등)를 함께 알려주세요.
답변은 명확하고 자연스러운 한국어로 작성하세요.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message["content"]