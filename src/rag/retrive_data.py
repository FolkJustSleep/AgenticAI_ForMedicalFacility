from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_data():
    DATAPATH = r"data/pdf"
    loader = PyPDFDirectoryLoader(DATAPATH)
    documents = loader.load()
    print(f"Loaded {len(documents)} documents from {DATAPATH}")
    return documents

def split_data(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100, separators=["\n\n", "\n", " ", ""])
    texts = text_splitter.split_documents(documents)
    print(f"Split into {len(texts)} chunks of text")
    # print(f"First text chunk: {texts[0].page_content}")
    return texts

if __name__ == "__main__":
    docs = load_data()
    texts = split_data(docs)
