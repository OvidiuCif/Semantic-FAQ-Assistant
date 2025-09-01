from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()
'''
take text and convert to 384 dimentional vector with openai text-embedding-3-small
these embeddings capture the semantic meaning of text and can be compared afterwards
'''

def get_embeddings(text):
    """generate embeddings for a given text using OpenAI's text-embedding-3-small model"""
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )
    return embeddings.embed_query(text)