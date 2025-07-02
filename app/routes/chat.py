from fastapi import APIRouter, Request
from pydantic import BaseModel
from app.services.retriever import retrieve_relevant_docs
from app.services.generator import generate_response

router = APIRouter()

class Question(BaseModel):
    query: str

@router.post("/ask")
async def ask_question(question: Question):
    docs = retrieve_relevant_docs(question.query)
    answer = generate_response(question.query, docs)
    return {"answer": answer}