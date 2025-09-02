from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()
'''
take text and convert to vector with openai embedding models
these embeddings capture the semantic meaning of text and can be compared afterwards
'''

def get_embeddings(text, model="text-embedding-3-small", dimensions=384):
    """generate embeddings for a given text using OpenAI's embedding models"""
    embeddings = OpenAIEmbeddings(
        model=model,
        dimensions=dimensions
    )
    return embeddings.embed_query(text)