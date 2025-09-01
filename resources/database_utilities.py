from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

'''
connection to the database & take an embedding and perform a search (similarity)
vector cosine similarity operator <=> and above threshold of 0.7
'''
def get_db_connection():
    load_dotenv()
    engine = create_engine(os.getenv('DATABASE_URL'))
    return engine

def search_similar_questions(query_embedding, engine, threshold=0.7):
    with engine.connect() as conn:
        result = conn.execute(text('''
            SELECT question, answer, 
                   1 - (embedding <=> :embedding) as similarity
            FROM faq_database_schema.faq_table
            WHERE 1 - (embedding <=> :embedding) > :threshold
            ORDER BY similarity DESC
            LIMIT 1;
        '''), {'embedding': query_embedding, 'threshold': threshold})
        return result.fetchone()