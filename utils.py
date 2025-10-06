
import os
# Set various user agent environment variables
os.environ["USER_AGENT"] = "my-language-app/1.0"

#  imports
from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import HuggingFacePipeline
from langchain.chains import RetrievalQA
from transformers import AutoTokenizer, pipeline, AutoModelForCausalLM
from langchain.prompts import PromptTemplate

import os
import warnings
# Suppress all deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

def setup_chain():
    # 1. Initialize the model
    model_id = "microsoft/DialoGPT-large"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id)

    # Add padding token
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    pipe = pipeline(
       "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=256,  # FIXED: max_new_token -> max_new_tokens
        temperature=0.7,
        pad_token_id=tokenizer.eos_token_id
    )
  
    llm = HuggingFacePipeline(pipeline=pipe)

    # 2. Setup the embedding model
    embeddings = HuggingFaceEmbeddings(
         model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return llm, embeddings

def process_document(document_path, is_url=True):
    llm, embeddings = setup_chain()

    # 3. Load the document
    if is_url:
        import requests
        from langchain_community.document_loaders import WebBaseLoader
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        loader = WebBaseLoader(document_path, requests_kwargs={"headers": headers})
    else:
        loader = PyPDFLoader(document_path)
    documents = loader.load()

    # 4. Split the text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)  
    texts = text_splitter.split_documents(documents)

    # 5. create the vector store
    vectorstore = Chroma.from_documents(documents=texts, embedding=embeddings)

    # 6. Create custom prompt to remove the default text
    custom_prompt = PromptTemplate(
        template="{context}\n\nQuestion: {query}\nAnswer:",
        input_variables=["context", "query"]
    )

    # 7. create the RetrievalQA chains
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(),
        return_source_documents=True  
    )
    return qa_chain

def ask_question(qa_chain, question):
    result = qa_chain({"query": question})
    return result["result"], result["source_documents"]