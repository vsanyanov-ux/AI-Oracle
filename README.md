# AI Oracle (Custom Router Agent)

This application is an AI-powered assistant capable of retrieving internal knowledge from a Supabase database (via vector embeddings) and looking up current events or dynamic data from the live internet using Google Search API. 

## Features
- **Local Embeddings**: Uses `sentence-transformers/all-MiniLM-L6-v2`.
- **Custom LLM Routing**: Analyzes the query to intuitively decide if the data exists locally or needs a web search.
- **RAG (Retrieval-Augmented Generation)**: Answers questions based on private company database context.
- **Web Fallback**: Connects to DuckDuckGo search to fetch live internet results without requiring any API keys.

## Setup
1. Create a virtual environment: `python -m venv venv`
2. Activate it: `venv\Scripts\Activate.ps1`
3. Install dependencies: `pip install -r requirements.txt` (or install manually: `fastapi`, `supabase`, `sentence-transformers`, `duckduckgo-search`, `langgraph`, etc.)
4. Set up a `.env` file with your credentials:
   - `SUPABASE_URL`
   - `SUPABASE_ANON_KEY`
   - `GIGACHAT_CREDENTIALS`
   - `GIGACHAT_SCOPE`

## Usage
Run the main script to test both knowledge base search and web search:
```bash
python app.py
```

## Tech Stack
- **Language**: Python
- **Database / Vector Store**: Supabase (pgvector)
- **Embeddings**: `sentence-transformers` (HuggingFace)
- **LLM Engine**: GigaChat via `langchain-gigachat`
- **Orchestration**: Custom prompt-based router inspired by LangChain/LangGraph architectures.
- **Web Search**: DuckDuckGo API (`duckduckgo-search`)

## What I Learned (As an AI Junior Developer)
Building this project taught me several key concepts about modern AI application architecture:
1. **RAG Mechanics**: I learned how to convert raw text into vector embeddings and store them in Supabase, then query them by semantic similarity rather than exact keyword matches.
2. **LLM Orchestration**: I discovered that you don't always need complex frameworks like LangChain's React Agent. A carefully crafted "Router Prompt" can effectively teach an LLM to choose between internal database knowledge and live web data on its own.
3. **Handling Dependencies**: Dealing with breaking changes between different API versions (like LangChain 0.2 vs 0.3) taught me the importance of reading library documentation and relying on stable underlying packages (like `requests` or `duckduckgo-search`) when library wrappers fail.
4. **Environment Security**: I learned how to properly use `.env` files and `.gitignore` to keep sensitive API keys (like Supabase and GigaChat credentials) secure and out of public GitHub repositories.
