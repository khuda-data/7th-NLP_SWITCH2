import json
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from app.utils.text_splitter import split_text

embedding = HuggingFaceEmbeddings(model_name="jhgan/ko-sbert-nli")
DB_PATH = "data/chroma"

docs = []
with open("data/documents.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        item = json.loads(line)
        split_docs = split_text(item["text"])
        docs.extend(split_docs)

Chroma.from_documents(docs, embedding, persist_directory=DB_PATH)
print(f"✅ Vector DB 저장 완료: {len(docs)} chunks")