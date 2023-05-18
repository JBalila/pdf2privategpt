from langchain.chains import RetrievalQA
from langchain.embeddings import LlamaCppEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.vectorstores import Chroma
from langchain.llms import GPT4All

def askQuery(query) -> str:        
    # Load stored vectorstore
    llama = LlamaCppEmbeddings(model_path="./privateGPT/models/ggml-model-q4_0.bin")
    persist_directory = 'db'
    db = Chroma(persist_directory=persist_directory, embedding_function=llama)
    retriever = db.as_retriever()

    # Prepare the LLM
    callbacks = [StreamingStdOutCallbackHandler()]
    llm = GPT4All(model='./privateGPT/models/ggml-gpt4all-j-v1.3-groovy.bin', backend='gptj', callbacks=callbacks, verbose=False)
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

    return queryResponse