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
    dim = embeddings.shape[1]

    if len(embeddings) < 100:
        index = faiss.IndexFlatL2(dim)
        index_type = "Flat"
    else:
        quantizer = faiss.IndexFlatL2(dim)
        nlist = min(100, len(embeddings))
        index = faiss.IndexIVFFlat(quantizer, dim, nlist)
        index.train(np.array(embeddings).astype("float32"))
        index_type = f"IVF (nlist={nlist})"

    index.add(np.array(embeddings).astype("float32"))

    os.makedirs(os.path.dirname(index_path), exist_ok=True)
    faiss.write_index(index, index_path)

    # Save metadata for retrieval
    metadata_path = os.path.join(os.path.dirname(index_path), "metadata.jsonl")
    with open(metadata_path, "w", encoding="utf-8") as f:
        for i, doc in enumerate(docs):
            doc["embedding_id"] = i
            f.write(json.dumps(doc, ensure_ascii=False) + "\n")

    print(f"Indexed {len(docs)} documents with dim={dim} using {index_type} index")
    print(f"Saved FAISS index to {index_path}")
    print(f"Saved metadata to {metadata_path}")

if __name__ == "__main__":
    build_faiss_index("data/combined_docs.jsonl", "embedding/faiss_index.bin")