def postprocess_response(response: str) -> str:
    # 예: 응답에서 "응답:\n" 부분 제거, JSON-like 구조 강제 등
    response = response.strip()

    if response.lower().startswith("answer:"):
        response = response[len("answer:"):].strip()

    # 필요 시 기타 정제 작업 추가
    return response