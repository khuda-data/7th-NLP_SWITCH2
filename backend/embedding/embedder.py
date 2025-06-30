# embedding/embedder.py
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
import os

def build_faiss_index(jsonl_path, index_path):
    model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    docs = []
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            docs.append(json.loads(line))

    texts = [doc["text"] for doc in docs]
    embeddings = model.encode(texts, show_progress_bar=True)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings).astype("float32"))

    os.makedirs(os.path.dirname(index_path), exist_ok=True)
    faiss.write_index(index, index_path)
    print(f"Saved FAISS index to {index_path}")

if __name__ == "__main__":
    build_faiss_index("data/combined_docs.jsonl", "embedding/faiss_index.bin")