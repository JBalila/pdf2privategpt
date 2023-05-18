from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import LlamaCppEmbeddings
import os
import time

TXT_FOLDER = os.path.join('TXT_FOLDER')

def feedToGPT(inputFile: str) -> None:
    startTime = time.time()
    inputPath = os.path.join(TXT_FOLDER, inputFile)

    # Load document and split in chunks
    loader = TextLoader(inputPath, encoding="utf8")
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)
    
    # Create embeddings
    llama = LlamaCppEmbeddings(model_path="./privateGPT/models/ggml-model-q4_0.bin")

    # Create and store locally vectorstore
    persist_directory = 'db'
    db = Chroma.from_documents(texts, llama, persist_directory=persist_directory)
    db.persist()
    db = None

    endTime = time.time()
    runtime = endTime - startTime
    print("Feeding to PrivateGPT: {:.4f} seconds".format(runtime))