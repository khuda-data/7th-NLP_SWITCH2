# app.py
from fastapi import FastAPI
from pydantic import BaseModel
from pipeline.rag_pipeline import rag_pipeline

app = FastAPI()

class Query(BaseModel):
    question: str

@app.post("/ask")
def ask_question(query: Query):
    answer = rag_pipeline(query.question)
    return {"answer": answer}