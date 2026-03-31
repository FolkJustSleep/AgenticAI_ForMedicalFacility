if __name__ != "__main__":
    from src.rag.retrive_data import load_data, split_texts, split_data, OCR_load_data
    from src.rag.embedding_data import embed_text, setup_chroma_db, query_chuncks
from langchain_ollama import ChatOllama
from dotenv import load_dotenv
import os

load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_HOST")

llm = ChatOllama(model="medllama2:7b", baseurl=OLLAMA_HOST)

def askllm(query: str, user_messages: str)-> tuple[str, Exception]:
    print("Asking LLM...")
    collection = setup_chroma_db()
    print(f"User message: {user_messages}")
    # PROMPT_CONTEXT = ""
    results = query_chuncks(query, collection)   
    PROMPT_CONTEXT = results['documents']
    print(f"Retrieved context: {PROMPT_CONTEXT}")
    messages = [
        (
            "system",
            f"""You are a helpful assistant that answer the user questions. Use the following context from the documents to provide accurate answers:\n
            This is the context you have retrieved from the documents:\n
            {PROMPT_CONTEXT} , if the question come with choice, please answer with the best one. if it doesn't come with choice, just answer the question based on the context and explain the context. if you don't know the answer, just say you don't know don't try to make up an answer.""",
        ),
        ("human", user_messages),
    ]
    try : 
        ai_msg = llm.invoke(messages)
        print(f"LLM Response: {ai_msg.content}")
        return ai_msg.content, None
    except Exception as e:
        print(f"Error during LLM invocation: {e}")
        return None, e


def setup_rag():
    # Load and split documents
    print("Setting up RAG...")
    collection = setup_chroma_db()
    exist_ids = collection.get()['ids']
    
    documents = OCR_load_data()
    # print(type(documents))

    # texts = split_data(documents)
    # print("Successfully split documents into chunks.")
    texts = split_texts(documents)
    # print("Text: ", texts[1:10])
    embedding = embed_text(texts)

    for i, text in enumerate(texts):
        if f"doc_{i}" in exist_ids:
            print(f"Document doc_{i} already exists in the database. Skipping insertion.")
            continue
        collection.upsert(
            ids=[f"doc_{i}"],
            documents=[text],
            embeddings=[embedding[i]]
        )
        print(f"Inserted document doc_{i} into the database.")
    # result = askllm("สิทธิหลักประกันสุขภาพแห่งชาติคืออะไร", collection)
    # print(f"LLM Response: {result}")
    return collection
if __name__ == "__main__":
    from retrive_data import load_data, split_texts, split_data, OCR_load_data
    from embedding_data import embed_text, setup_chroma_db, query_chuncks
    print("Running RAG setup...")
    collection = setup_rag()