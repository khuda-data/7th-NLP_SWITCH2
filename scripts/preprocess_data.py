import pandas as pd
import json

INPUT_CSV = "data/data.csv"
OUTPUT_JSONL = "data/documents.jsonl"

def format_row(row):
    return {
        "id": row.name,
        "text": f"제목: {row['title']}\n주최: {row['host']}\n기간: {row['date']}\n설명: {row['description']}\n링크: {row['url']}"
    }

df = pd.read_csv(INPUT_CSV)
documents = [format_row(row) for _, row in df.iterrows()]

with open(OUTPUT_JSONL, "w", encoding="utf-8") as f:
    for doc in documents:
        f.write(json.dumps(doc, ensure_ascii=False) + "\n")

print(f"✅ 총 {len(documents)}개의 문서를 저장했습니다.")