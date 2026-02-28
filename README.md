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
