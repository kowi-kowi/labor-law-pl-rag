from fastapi import FastAPI
from pydantic import BaseModel
from retrieval import retrieve_context, ask_llm

app = FastAPI(title="Polish Labor Law AI Assistant")

class Query(BaseModel):
    question: str

@app.post("/ask")
def ask(query: Query):
    context = retrieve_context(query.question)
    answer = ask_llm(query.question, context)
    return {"answer": answer}