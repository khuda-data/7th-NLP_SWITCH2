import requests
import json

OLLAMA_BASE = "http://localhost:11434"

def generate_with_llama(prompt):
    payload = {"model": "llama3.1:8b", "prompt": prompt}
    response = requests.post(f"{OLLAMA_BASE}/api/generate", json=payload, stream=True)

    output = ""
    try:
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode("utf-8"))
                    if "response" in data:
                        output += data["response"]
                except json.JSONDecodeError:
                    continue
        return output if output else "응답 없음"
    except Exception as e:
        return f"예외 발생: {str(e)}"