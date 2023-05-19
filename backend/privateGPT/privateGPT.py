import os
import time
from folderLocations import PRIVAGEGPT_FOLDER, DB_FOLDER

from langchain.chains import RetrievalQA
from langchain.embeddings import LlamaCppEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.vectorstores import Chroma
from langchain.llms import GPT4All

def askQuery(query) -> str:
    # See how long program takes to run
    startTime = time.time()

    # Load stored vectorstore
    llama = LlamaCppEmbeddings(model_path=os.path.join(PRIVAGEGPT_FOLDER, 'models', 'ggml-model-q4_0.bin'))
    persist_directory = DB_FOLDER
    db = Chroma(persist_directory=persist_directory, embedding_function=llama)
    retriever = db.as_retriever()

    # Prepare the LLM
    callbacks = [StreamingStdOutCallbackHandler()]
    llm = GPT4All(model=os.path.join(PRIVAGEGPT_FOLDER, 'models', 'ggml-gpt4all-j-v1.3-groovy.bin'), backend='gptj', callbacks=callbacks, verbose=False)
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True)

    # Store response in <queryResponse>
    queryResponse = ''
    
    # Get the answer from the chain
    res = qa(query)
    answer, docs = res['result'], res['source_documents']

    # Store result
    queryResponse += answer
    
    # Print the relevant sources used for the answer
    for document in docs:
        queryResponse += ('\n<1>: ')
        queryResponse += document.page_content
    
    # Output program time
    endTime = time.time()
    runtime = endTime - startTime
    print("Feeding to PrivateGPT: {:.4f} seconds".format(runtime))

    return queryResponse