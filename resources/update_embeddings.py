from database_utilities import get_db_connection
from embedding_utilities import get_embeddings
from sqlalchemy import text

def update_faq_embeddings():
    print("conn to database")
    engine = get_db_connection()
    
    with engine.connect() as conn:
    #get all FAQs without embeddings
        print("get faqs without embeddings")
        result = conn.execute(text('''
            SELECT id, question 
            FROM faq_database_schema.faq_table 
            WHERE embedding IS NULL
        '''))
    ###    
        faqs = result.fetchall()
        total = len(faqs)
        print(f"found: {total} faqs without embeddings")
        
        for i, (faq_id, question) in enumerate(faqs, 1):
            print(f"Processing: {i}/{total}: {question[:30]}")
            embedding = get_embeddings(question)
            
            conn.execute(text('''
                UPDATE faq_database_schema.faq_table 
                SET embedding = :embedding 
                WHERE id = :id
            '''), {'embedding': embedding, 'id': faq_id})
            conn.commit()
            print(f"Updated embedding for FAQ #{faq_id}")

if __name__ == "__main__":
    update_faq_embeddings()