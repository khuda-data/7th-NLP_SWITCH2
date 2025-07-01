# app.py
from fastapi import FastAPI
from pydantic import BaseModel
from pipeline.rag_pipeline import rag_pipeline
from pipeline.llama_pipeline import llama_pipeline
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 혹은 ["http://localhost:3000"] 등 필요한 도메인
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class Query(BaseModel):
    question: str

@app.post("/ask")
def ask_question(query: Query):
    answer = llama_pipeline(query.question)
    return {"answer": answer}