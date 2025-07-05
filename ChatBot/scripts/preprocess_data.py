import pandas as pd
import json

INPUT_CSV = "data/data.csv"
OUTPUT_JSONL = "data/documents.jsonl"

def format_row(row):
    # 실제 컬럼명을 확인하여 처리
    try:
        return {
            "id": row.name,
            "title": row.get('제목', row.get('title', '')),
            "host": row.get('주최', row.get('host', '')),
            "date": row.get('기간', row.get('date', '')),
            "description": row.get('설명', row.get('description', '')),
            "url": row.get('링크', row.get('url', '')),
            "category": row.get('카테고리', row.get('category', ''))
        }
    except Exception as e:
        print(f"❌ Error formatting row {row.name}: {e}")
        return None

df = pd.read_csv(INPUT_CSV)
print(f"📄 CSV columns: {df.columns.tolist()}")
documents = [doc for _, row in df.iterrows() if (doc := format_row(row))]

with open(OUTPUT_JSONL, "w", encoding="utf-8") as f:
    for doc in documents:
        f.write(json.dumps(doc, ensure_ascii=False) + "\n")

print(f"✅ 총 {len(documents)}개의 문서를 저장했습니다.")