from typing import Union
import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
# from src.rag.rag import askllm
from src.rag.embedding_data import setup_chroma_db
from src.service.LLM_logic import AgentsicAI
from src.service.AskLLM import generate_answer
from model.chat_test import ChatTestRequest, ChatTestResponse
import src.gateway.Line_gateway as gateway 
from data.postgres import get_connection
# print("Starting RAG setup...")

app = FastAPI()
conn = get_connection()
if conn == False:
    print("Failed to connect to the database.")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/ask", response_model=ChatTestResponse)
def chat_endpoint(user_message: ChatTestRequest):
    chat_response, err = generate_answer(user_message.message)
    if err != None:
        Error_message = f"Error in generate_answer: {err}"
        print(Error_message)
        return ChatTestResponse(response=Error_message, status_code=500)
    return ChatTestResponse(response=chat_response)

@app.post("/chat", response_model=ChatTestResponse)
def chat_endpoint(user_message: ChatTestRequest):
    AgentsicAI_response, err = AgentsicAI(user_message.message)
    if err != None:
        return ChatTestResponse(response=str(err), status_code=500)
    return ChatTestResponse(response=AgentsicAI_response)

@app.post("/webhook/line-webhook", response_model=ChatTestResponse)
def line_webhook(event: dict):
    response , err = gateway.Handle_line_webhook(event)
    if err is not None:
        return ChatTestResponse(response=str(err), status_code=500)
    return ChatTestResponse(response=response, status_code=200)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=os.getenv("PORT", 8000))