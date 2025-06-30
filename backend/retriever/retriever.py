# retriever/retriever.py
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json

model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
index = faiss.read_index("embedding/faiss_index.bin")

with open("data/combined_docs.jsonl", "r", encoding="utf-8") as f:
    docs = [json.loads(line) for line in f]

def retrieve(query, top_k=3):
    query_vec = model.encode([query])
    D, I = index.search(np.array(query_vec).astype("float32"), top_k)
    return [docs[i]["text"] for i in I[0]]