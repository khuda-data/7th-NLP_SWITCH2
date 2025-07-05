from fastapi import APIRouter, Request
from pydantic import BaseModel
from app.services.retriever import retrieve_relevant_docs
from app.services.generator import generate_response

import logging

router = APIRouter()
logging.basicConfig(level=logging.INFO)

class Question(BaseModel):
    query: str

@router.post("/ask")
async def ask_question(question: Question):
    docs = retrieve_relevant_docs(question.query)
    logging.info(f"Retrieved documents: {docs}")

    if not docs:
        return {"answer": "관련된 문서를 찾을 수 없습니다."}

    answer = generate_response(question.query, docs)
    return {"answer": answer}