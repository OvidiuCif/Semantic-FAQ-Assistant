## Semantic FAQ Assistant

A semantic search system that uses OpenAI embeddings to find relevant FAQ answers and generates responses using GPT models - included PostgreSQL integration for embeddings.  Both CLI interface and REST API with JWT authentication - Docker setup is also done for avoiding postgresql and pgvector installation process.

## Overview - Process Map
```mermaid
graph TB
    A[User Input] --> B{Interface}
    B -->|CLI| C[main.py]
    B -->|API| D[api.py + Auth via HTTP call]
    
    C --> E[chat_logic.py]
    D --> E
    
    E --> F[embedding_utilities.py]
    E --> G[database_utilities.py]
    
    F --> H[OpenAI Embeddings API]
    G --> I[(PostgreSQL + pgvector)]
    
    E --> J[OpenAI GPT API]
    
    I --> K[Vector Similarity Search]
    K --> E
    
    E --> L[Generated Response]
    L --> M[User]
```

## Local Setup
### Prerequisites
- python 3.11
- PostgreSQL 17
- OpenAI key

### Setup Steps
1. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

2. Install PostgreSQL (version 17 -development)
```bash
winget install PostgreSQL.PostgreSQL
```

3. Install pgvector extension (via cmd)
```bash
set PGROOT=C:\Program Files\PostgreSQL\17
set PATH=C:\Program Files\PostgreSQL\17\bin;%PATH%
set PG_CONFIG=C:\Program Files\PostgreSQL\17\bin\pg_config

#init VS Build Tools
"C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat"

#build and install pgvector
cd C:\temp\pgvector\pgvector-0.5.1
nmake /f Makefile.win
nmake /f Makefile.win install
```

4. Create db/tables
Run the PostgreSQL.sql script to create the database schema and insert FAQ data - adjust with different insert(data) or names

5. Create .env file
```
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/faq_database
JWT_SECRET_KEY=your_jwt_secret_here
API_PASSWORD=your_api_password_here -- to be used in API call
```

6. Generate embeddings
```bash
python resources/update_embeddings.py
```
This connects to the database, finds FAQ entries without embeddings, generates embeddings using OpenAI and updates the database

7. Run the application
```bash
# CLI version
python main.py

# API version
python api.py
```

## Docker setup 
### requirements
- Docker desktop

### setup Steps
1. create .env file (layout mentioned above)

2. start containers
```bash
docker-compose up -d
```

3. generate embeddings
```bash
docker-compose exec app python resources/update_embeddings.py
```

4. Access API at http://localhost:8000/docs

## API usage
### auth
1. Get access token from `/token` endpoint
    body:
   - username: `api_user`
   - password: value from API_PASSWORD in your .env

2. Use token in Authorization header
   ```
   Authorization: Bearer <value>
   ```

### Ask question/use chatbot
POST to `/ask-question` with:
```json
{
  "question_text": "my questions",
  "model": "gpt-4o-mini",
  "temperature": 0.7,
  "similarity_threshold": 0.7,
  "embedding_model": "text-embedding-3-small"
}
```

## How it works (high-level)
1. you submit a question via CLI or API
2. system generates embedding for the question using OpenAI
3. cector similarity search finds most relevant FAQ in PostgreSQL db
4. if - similarity above threshold, GPT generates response based on FAQ context
5. response returned to user
6. user input/or terminate

## File structure
- main.py - CLI interface
- api.py - REST API/auth
- chat_logic.py - core question processing logic
- api_security.py - JWT authentication
- database_utilities.py - db operations
- embedding_utilities.py -openAI embedding operations
- update_embeddings.py -populate embeddings
- PostgreSQL.sql - db schema and sample data

## other notes
-  embeddings column is initially empty when you create the database
-  run update_embeddings.py to populate embeddings for existing FAQ entries
- db(postgresSQL) and OpenAI key must be configured in .env file
- doccker setup eliminates the complex PostgreSQL + pgvector installation process
