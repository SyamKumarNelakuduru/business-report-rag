from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class AskRequest(BaseModel):
    question: str

@app.get("/")
def home():
    return {"message": "Backend is running 🚀"}

@app.get("/health")
def health():
    return {"status": "OK"}

@app.post("/ask")
def ask_question(request: AskRequest):
    return {
        "question": request.question,
        "answer": f"You asked: {request.question}"
    }