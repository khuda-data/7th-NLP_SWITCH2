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

                이 정보를 바탕으로 사용자에게 유용한 답변을 생성하세요.
                """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message["content"]