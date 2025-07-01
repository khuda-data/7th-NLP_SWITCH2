# utils/combine_csv.py
import pandas as pd
import json
import os

def convert_csv_to_jsonl():
    input_path = "data/data.csv"
    output_path = "data/combined_docs.jsonl"
    combined = []

    df = pd.read_csv(input_path)
    df["source"] = "data.csv"
    doc_id = 0

    for _, row in df.iterrows():
        title = str(row.get("title", "")).strip()
        date = str(row.get("date", "")).strip()
        host = str(row.get("host", "")).strip()
        description = str(row.get("description", "")).strip()

        # 키워드 기반 요약 text 구성
        keyword_text = f"title: {title} | host: {host} | date: {date} | keywords: {description[:150]}"

        combined.append({
            "id": doc_id,
            "text": keyword_text,
            "source": "data.csv"
        })
        doc_id += 1

    os.makedirs("data", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for doc in combined:
            f.write(json.dumps(doc, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    convert_csv_to_jsonl()