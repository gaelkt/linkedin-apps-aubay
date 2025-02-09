from langchain_qdrant import FastEmbedSparse
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_openai import OpenAI
#from langchain.llms import OpenAI

#pip install -U langchain-openai


import os

def set_llm(model="openai"):

    if model == "openai":
        llm = OpenAI(api_key=os.environ['OPENAI_API_KEY'], temperature=0)
    
    elif model == "ollana":
        llm = OllamaLLM(model="llama3.2", temperature=0.0)
    
    else:
        raise Exception("Invalid llm model")

    return llm

def set_embeddings(model):

    # Dense embedings
    if model == "BAAI/bge-base-en-v1.5":
        model_kwargs = {'device':'cpu'}
        encode_kwargs = {'normalize_embeddings': True}

        generate_embeddings = HuggingFaceEmbeddings(
        model_name=model,     
        model_kwargs=model_kwargs, 
        encode_kwargs=encode_kwargs)

    # Dense embedings
    elif model == "openai":
        generate_embeddings=OpenAIEmbeddings()

    # Dense embedings
    elif model == "text-embedding-3-large":
        generate_embeddings=OpenAIEmbeddings(model="text-embedding-3-large")

    # Sparse embedings
    elif model == "Qdrant/bm25":
        generate_embeddings=FastEmbedSparse(model_name="Qdrant/bm25")

    # Sparse embedings
    elif model == "prithivida/Splade_PP_en_v1":
        generate_embeddings=FastEmbedSparse(model_name="prithivida/Splade_PP_en_v1")


    return generate_embeddings

def embeddings(model):

    # Dense embedings
    if model == "BAAI/bge-base-en-v1.5":
        model_kwargs = {'device':'cpu'}
        encode_kwargs = {'normalize_embeddings': True}

        generate_embeddings = HuggingFaceEmbeddings(
        model_name=model,     
        model_kwargs=model_kwargs, 
        encode_kwargs=encode_kwargs)

    # Dense embedings
    elif model == "openai":
        generate_embeddings=OpenAIEmbeddings()

    # Dense embedings
    elif model == "text-embedding-3-large":
        generate_embeddings=OpenAIEmbeddings(model="text-embedding-3-large")

    # Sparse embedings
    elif model == "Qdrant/bm25":
        generate_embeddings=FastEmbedSparse(model_name="Qdrant/bm25")

    # Sparse embedings
    elif model == "Qdrant/bm25":
        generate_embeddings=FastEmbedSparse(model_name="prithivida/Splade_PP_en_v1")


    return generate_embeddings