from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
from resources.database_utilities import get_db_connection, search_similar_questions
from resources.embedding_utilities import get_embeddings
load_dotenv()

def create_chat():
    llm = ChatOpenAI(
        model_name="gpt-4o-mini",
        temperature=0.7, #to further check other params
    )
    prompt = ChatPromptTemplate.from_template(
        """You are a helpful assistant who answers users questions clearly and on point.
        FAQ Database Answer: {faq_answer}    
        Question: {question}
        If the FAQ Database Answer is relevant to the question, use that information to answer.
        If the FAQ Database Answer is "No relevant FAQ found", answer the question using your general knowledge.
        Keep responses concise and helpful and do not add emojis."""
    )
    chain = LLMChain(llm=llm, prompt=prompt)  
    return chain

def main():
    chain = create_chat()
    engine = get_db_connection()
    print("\nSemantic FAQ Assistant initialized.\n Type 'quit', 'exit', 'bye', or 'close' to end,\nHave fun!")

    while True:
        user_input = input("\nYou: ...")
        if user_input.lower() in ['quit', 'exit', 'bye', 'close']:
            break
            
        try:
            #generate embeddings for the user's question
            query_embedding = get_embeddings(user_input)
            #search for similar questions in the FAQ database
            result = search_similar_questions(query_embedding, engine)
            
            if result:
                question, answer, similarity = result
                print(f"[Found similar FAQ with {similarity:.2f} similarity]")
                faq_answer = answer
            else:
                print("[No relevant FAQ found]")
                faq_answer = "No relevant FAQ found"
            
            #llm - chain with the retrieved faq-answer
            response = chain.invoke({
                "question": user_input,
                "faq_answer": faq_answer
            })       
            print("\nSemantic-FAQ-Assistant:", response['text'])
            
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()