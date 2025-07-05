import json
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.docstore.document import Document
import sys
import os
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGCHAIN_ENDPOINT"] = ""
os.environ["LANGCHAIN_API_KEY"] = ""
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from app.utils.text_splitter import split_text

embedding = HuggingFaceEmbeddings(model_name="jhgan/ko-sbert-nli")
DB_PATH = "data/chroma"

docs = []
with open("data/documents.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        item = json.loads(line)
        # title과 description을 합쳐서 벡터화
        text = f"{item.get('title', '')}\n\n{item.get('description', '')}"
        split_texts = split_text(text)
        for chunk in split_texts:
            doc = Document(
                page_content=chunk.page_content,
                metadata={
                    "id": item.get("id", ""),
                    "title": item.get("title", ""),
                    "date": item.get("date", ""),
                    "host": item.get("host", ""),
                    "url": item.get("url", ""),
                    "category": item.get("category", "")
                }
            )
            docs.append(doc)

Chroma.from_documents(docs, embedding, persist_directory=DB_PATH)
print(f"✅ Vector DB 저장 완료: {len(docs)} chunks")