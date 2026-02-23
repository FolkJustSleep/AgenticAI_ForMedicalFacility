import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typhoon_ocr import ocr_document

load_dotenv()

def load_data():
    DATAPATH = r"data/pdf"
    # loader = PyPDFDirectoryLoader(DATAPATH)
    # documents = loader.load()
    # print(f"Loaded {len(documents)} documents from {DATAPATH}")
    documents = []
    pagenum = [32, 270, 62]
    for i, dir_name in enumerate(os.listdir(DATAPATH)):
        print(f"Processing {os.path.join(DATAPATH, dir_name)}...")# Limit to processing only the first document for testing
        texts = ocr_document(os.path.join(DATAPATH, dir_name), page_num=pagenum[i])
        documents.extend(texts)
    return documents

def split_data(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100, separators=["\n\n", "\n", " ", ""])
    texts = text_splitter.split_documents(documents)
    print(f"Split into {len(texts)} chunks of text")
    # print(f"First text chunk: {texts[0].page_content}")
    return texts

def split_texts(texts) -> list[str]:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100, separators=["\n\n", "\n", " ", ""])
    all_split_texts = []
    for text in texts:
        split_texts = text_splitter.split_text(text)
        all_split_texts.extend(split_texts) # append is used to add a single element to the list, while extend is used to add multiple elements from another list to the existing list.
    print(f"Split into {len(all_split_texts)} chunks of text")
    # print(f"First split text chunk: {all_split_texts[0]}")
    return all_split_texts

if __name__ == "__main__":
    docs = load_data()
    text = split_texts(docs)