from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from typing import Optional
from resources.database_utilities import get_db_connection
from modules.chat_logic import *
from modules.api_security import *
from datetime import timedelta
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(
    title="Semantic FAQ Assistant API",
    description="API for semantic FAQ searches with JWT authentication",
    version="1.0.0"
)

#init db conn
engine = get_db_connection()

class QuestionRequest(BaseModel):
    question_text: str
    model: str = Field(default=DEFAULT_MODEL, description="Model to use (ex: gpt-4o-mini, gpt-4o)")
    temperature: float = Field(default=DEFAULT_TEMPERATURE, ge=0, le=2.0, description="Temperature for response generation")
    similarity_threshold: float = Field(default=DEFAULT_SIMILARITY_THRESHOLD, ge=0, le=1.0, description="Minimum similarity threshold")
    custom_prompt: Optional[str] = Field(default=None, description="Custom prompt template")
    embedding_model: str = Field(default=DEFAULT_EMBEDDING_MODEL, description="Embedding model to use")
    embedding_dimensions: int = Field(default=DEFAULT_EMBEDDING_DIMENSIONS, description="Embedding dimensions")

#endpoint to get access token/auth --
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Get an access token by providing username and password
    """
    #(hardcoded for dev/test)
    if form_data.username != "api_user" or form_data.password != os.environ.get("API_PASSWORD", "default_password"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
#30-minute expiration
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

#JWT authentication - added
@app.post("/ask-question")
async def ask_question(
    request: QuestionRequest,
    current_user: str = Depends(get_current_user)
):
    """
    Ask a question to the semantic FAQ system (requires authentication)
    """
    try:
        response = process_user_query(
            user_input=request.question_text,
            engine=engine,
            similarity_threshold=request.similarity_threshold,
            model_name=request.model,
            temperature=request.temperature,
            custom_prompt=request.custom_prompt,
            embedding_model=request.embedding_model,
            embedding_dimensions=request.embedding_dimensions
        )
        
        return response      
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)