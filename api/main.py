from fastapi import FastAPI
from pydantic import BaseModel
from orchestration.rag_chain import build_rag_chain

app = FastAPI()

rag = build_rag_chain()


class QueryRequest(BaseModel):
    question: str


@app.post("/query")
def query_rag(request: QueryRequest):

    result = rag.run(request.question)

    return result