from app.services.prompt_template import build_prompt
from app.llama.lama import generate_with_llama
from app.utils.postprocess import postprocess_response
def generate_response(question, docs):
    prompt = build_prompt(question, docs)
    response = generate_with_llama(prompt)
    cleaned = postprocess_response(response)  # 후처리 함수 적용
    return cleaned