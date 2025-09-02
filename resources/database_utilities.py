# filepath: c:\Projects\Semantic FAQ Assistant\resources\database_utilities.py
from sqlalchemy import create_engine, text
import os

'''
connection to the database & take an embedding and perform a search (similarity)
vector cosine similarity operator <=> and above threshold of 0.7
'''
def get_db_connection():
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        raise ValueError("Database URL is not set in the .env file")
    return create_engine(database_url)

def search_similar_questions(query_embedding, engine, threshold=0.7):
    '''
    search for similar questions in the db using vector-similarity
    '''
    try:
        with engine.connect() as conn:
            embedding_str = str(query_embedding).replace('[', '').replace(']', '')
            
            result = conn.execute(
                text(
                """
                SELECT question, answer,
                        1 - (embedding <=> '[""" + embedding_str + """]'::vector) as similarity
                FROM faq_database_schema.faq_table
                WHERE 1 - (embedding <=> '[""" + embedding_str + """]'::vector) > :threshold
                ORDER BY similarity DESC
                LIMIT 1;
                """),
                {"threshold": threshold}
            )
            
            row = result.fetchone()
            if row:
                return row[0], row[1], row[2]
            return None
    except Exception as e:
        print(f"Database search error: {str(e)}")
        return None