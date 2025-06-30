# utils/combine_csv.py
import pandas as pd
import json
import os

def combine_csvs():
    files = ["dacon_competitions.csv", "dev_events.csv", "wevity_events.csv"]
    output_path = "data/combined_docs.jsonl"
    combined = []

    for fname in files:
        df = pd.read_csv(f"data/{fname}")
        df["source"] = fname
        for _, row in df.iterrows():
            content = " | ".join([f"{col}: {str(row[col])}" for col in df.columns])
            combined.append({"id": len(combined), "text": content})

    os.makedirs("data", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for doc in combined:
            f.write(json.dumps(doc, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    combine_csvs()