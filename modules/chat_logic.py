from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

load_dotenv()

DEFAULT_PROMPT = """You are a helpful assistant who answers users questions clearly and on point.
FAQ Database Answer: {faq_answer}    
Question: {question}
If the FAQ Database Answer is relevant to the question, use that information to answer.
If the FAQ Database Answer is "No relevant FAQ found", answer the question using your general knowledge.
Keep responses concise and helpful and do not add emojis."""
DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_SIMILARITY_THRESHOLD = 0.7
DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"
DEFAULT_EMBEDDING_DIMENSIONS = 384 #not sure if this is needed as param -- as db need to reflect schema

def create_chat(model_name=DEFAULT_MODEL, temperature=DEFAULT_TEMPERATURE, custom_prompt=None):
    """chat chain with the specified parameters"""
    llm = ChatOpenAI(
        model_name=model_name,
        temperature=temperature,
    )
    prompt_template = custom_prompt if custom_prompt else DEFAULT_PROMPT
    prompt = ChatPromptTemplate.from_template(prompt_template)
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain

def process_user_query(user_input, engine, similarity_threshold=DEFAULT_SIMILARITY_THRESHOLD, 
                       model_name=DEFAULT_MODEL, temperature=DEFAULT_TEMPERATURE, custom_prompt=None,
                       embedding_model=DEFAULT_EMBEDDING_MODEL, embedding_dimensions=DEFAULT_EMBEDDING_DIMENSIONS):
    from resources.embedding_utilities import get_embeddings
    from resources.database_utilities import search_similar_questions
    
    #chat chain
    chain = create_chat(model_name, temperature, custom_prompt)
    
    #generate embeddings for the user question
    query_embedding = get_embeddings(user_input, model=embedding_model, dimensions=embedding_dimensions)

    #search similarity
    result = search_similar_questions(query_embedding, engine, threshold=similarity_threshold)
    
    if result:
        question, answer, similarity = result
        response_data = {
            "matched_faq": question,
            "faq_answer": answer,
            "similarity": similarity,
            "used_faq": True
        }
    else:
        response_data = {
            "matched_faq": None,
            "faq_answer": "No relevant answer found in the FAQ database",
            "similarity": 0,
            "used_faq": False
        }
    
    #generic/ response using LLM
    llm_response = chain.invoke({
        "question": user_input,
        "faq_answer": response_data["faq_answer"]
    })
    
    response_data["answer"] = llm_response["text"]
    response_data["model_used"] = model_name
    response_data["temperature_used"] = temperature
    response_data["embedding_model_used"] = embedding_model
    response_data["embedding_dimensions_used"] = embedding_dimensions
    
    return response_data