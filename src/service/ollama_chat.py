# from langchain_ollama import ChatOllama
from langchain_ollama import ChatOllama
from typing import Union
import os
# import dotenv

# dotenv.load_dotenv()
OLLAMA_HOST = os.getenv("OLLAMA_HOST")
print(f"OLLAMA_HOST: {OLLAMA_HOST}")

# llm = ChatOllama(model="medllama2", baseurl="http://localhost:11434")

llm = ChatOllama(model="medllama2:7b", baseurl=OLLAMA_HOST)
def chat(user_messages: str) -> Union[str, None]:
    print(f"User message: {user_messages}")
    messages = [
        (
            "system",
            "You are a helpful assistant that answer the user questions about medical.",
        ),
        ("human", user_messages),
    ]
    try :
        ai_msg = llm.invoke(messages)
        return ai_msg.content, None
    except Exception as e:
        print(f"Error during LLM invocation: {e}")
        return None, e