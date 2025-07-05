from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# 벡터 DB 경로
DB_PATH = "data/chroma"

# 동일한 임베딩 사용
embedding = HuggingFaceEmbeddings(model_name="jhgan/ko-sbert-nli")

# DB 로드
db = Chroma(persist_directory=DB_PATH, embedding_function=embedding)

# 쿼리
query = "AI 윤리와 관련된 공모전"
results = db.similarity_search(query, k=3)

for i, doc in enumerate(results, 1):
    print(f"--- 결과 {i} ---")
    print(doc.page_content)