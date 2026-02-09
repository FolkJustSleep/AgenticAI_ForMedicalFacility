from typing import Union
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from src.rag.rag import askllm
from src.rag.embedding_data import setup_chroma_db
# from fastapi.encoders import jsonable_encoder
from src.service.ollama_chat import chat
from model.chat_test import ChatTestRequest, ChatTestResponse

# print("Starting RAG setup...")
collection = setup_chroma_db()
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/ask", response_model=ChatTestResponse)
def chat_endpoint(user_message: ChatTestRequest):
    chat_response, err = askllm(user_message.message, collection)
    if err is not None:
        return JSONResponse( status_code=500)
    return ChatTestResponse(response=chat_response)

@app.post("/chat", response_model=ChatTestResponse)
def chat_endpoint(user_message: ChatTestRequest):
    chat_response, err = chat(user_message.message)
    if err is not None:
        return JSONResponse(content={"error": str(err)}, status_code=500)
    return ChatTestResponse(response=chat_response)