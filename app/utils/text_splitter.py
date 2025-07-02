from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_text(document: str):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.create_documents([document])