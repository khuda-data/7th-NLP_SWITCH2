import json
import re

def extract_date_from_context(context):
    """
    문서 내용에서 ■ 접수기간 ~ 형태의 날짜를 찾아 반환.
    없으면 None
    """
    match = re.search(r"접수\s*기간[^\d]*(\d{4}[^■\n]*)", context)
    if match:
        return match.group(1).strip()
    return None

def postprocess_response(response: str, context: str, as_text=True):
    response = response.strip()
    if response.lower().startswith("answer:"):
        response = response[len("answer:"):].strip()

    try:
        data = json.loads(response)
    except Exception:
        return response if as_text else None

    if isinstance(data, dict):
        data = [data]

    for item in data:
        if not isinstance(item, dict):
            continue
        if item.get("date", "").strip() in ("", "알 수 없음"):
            extracted_date = extract_date_from_context(context)
            if extracted_date:
                item["date"] = extracted_date

    if not as_text:
        return data

    output = []

    for idx, item in enumerate(data, 1):
        cleaned_item = {
            k: v for k, v in item.items()
            if v and str(v).strip() not in ("", "null", "None")
        }
        output.append(f"[공모전 {idx}]")
        for k, v in cleaned_item.items():
            output.append(f"- {k}: {v}")
        output.append("")

    return "\n".join(output) if output else "관련된 공모전 정보를 찾을 수 없습니다."