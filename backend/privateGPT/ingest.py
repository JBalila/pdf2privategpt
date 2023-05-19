import os
import time
from folderLocations import TXT_FOLDER, PRIVAGEGPT_FOLDER, DB_FOLDER

from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import LlamaCppEmbeddings

def feedToGPT(inputFile: str) -> None:
    inputPath = os.path.join(TXT_FOLDER, inputFile)

    # Load document and split in chunks
    loader = TextLoader(inputPath, encoding="utf8")
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)
    
    # TODO: Speed this up
    # Create embeddings
    startTime = time.time()
    llama = LlamaCppEmbeddings(model_path=os.path.join(PRIVAGEGPT_FOLDER, 'models', 'ggml-model-q4_0.bin'))
    endTime = time.time()
    print("Creating embeddings: {:.4f} seconds".format(endTime-startTime))

    # TODO: Parallelize this
    # Create and store locally vectorstore
    startTime = time.time()
    persist_directory = DB_FOLDER
    db = Chroma.from_documents(texts, llama, persist_directory=persist_directory)
    db.persist()
    db = None
    endTime = time.time()
    print("Creating vectorstore: {:.4f} seconds".format(endTime-startTime))