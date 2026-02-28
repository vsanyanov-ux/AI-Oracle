import os
from dotenv import load_dotenv
from supabase import create_client, Client
from sentence_transformers import SentenceTransformer
from llm import llm
import requests
from langchain_core.prompts import PromptTemplate

# Load environment variables first
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


# Локальная модель эмбеддингов (можно поменять на другую)
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def embed(text: str) -> list[float]:
    vec = model.encode(text)
    return vec.tolist()

def search(query: str, match_threshold: float = 0.5, match_count: int = 5):
    query_embedding = embed(query)

    # ВАЖНО: оборачиваем в try/except вместо res.error
    try:
        res = supabase.rpc(
            "match_docs",
            {
                "query_embedding": query_embedding,
                "match_threshold": match_threshold,
                "match_count": match_count,
            },
        ).execute()
    except Exception as e:
        print("Search RPC error:", e)
        return []

    # В новой версии .data лежит прямо в res.data
    docs = res.data or []

    for d in docs:
        print("---")
        print("similarity:", d.get("similarity"))
        print("content:", d.get("content")[:200], "...")
    return docs

def web_search_direct(query: str) -> str:
    """Useful for answering questions about current events or general knowledge."""
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        return "Web search is currently unavailable. Please add SERPAPI_API_KEY to your .env file."
    
    try:
        url = "https://serpapi.com/search"
        params = {
            "q": query,
            "api_key": api_key,
            "engine": "google"
        }
        res = requests.get(url, params=params)
        res.raise_for_status()
        data = res.json()
        
        if "answer_box" in data and "answer" in data["answer_box"]:
            return data["answer_box"]["answer"]
        if "answer_box" in data and "snippet" in data["answer_box"]:
            return data["answer_box"]["snippet"]
        if "organic_results" in data and len(data["organic_results"]) > 0:
            return data["organic_results"][0].get("snippet", "No snippet available.")
            
        return "No direct answer found on the web."
    except Exception as e:
        return f"Error performing web search: {e}"

def route_query(query: str) -> str:
    """Asks the LLM to decide if this query needs a web search or local database search."""
    routing_prompt = PromptTemplate.from_template(
        "You are a routing assistant. Your job is to decide if a user's query requires searching the live internet or if it can be answered using an internal company database.\n"
        "If the query asks about current events, live data (like weather, sports scores, current news), or general world knowledge not specific to a company, respond with ONLY the word: WEB\n"
        "If the query asks about company policies, specific internal documentation, definitions like 'what is a RAG system', or if you are unsure, respond with ONLY the word: DB\n\n"
        "User Query: {query}\n"
        "Decision (WEB or DB):"
    )
    decision = llm.invoke(routing_prompt.format(query=query)).content.strip().upper()
    return "WEB" if "WEB" in decision else "DB"

def ask_oracle(query: str, top_n: int = 3) -> str:
    route = route_query(query)
    
    if route == "WEB":
        print(f"--> LLM Router chose: INTERNET SEARCH")
        web_context = web_search_direct(query)
        final_prompt = PromptTemplate.from_template(
            "Answer the user's question based on the following information from the internet.\n\n"
            "Internet Context: {context}\n\n"
            "User Question: {query}\n"
        )
        return llm.invoke(final_prompt.format(context=web_context, query=query)).content
    else:
        print(f"--> LLM Router chose: DATABASE SEARCH")
        docs = search(query, match_count=top_n)
        if not docs:
            # Fallback to web search if DB fails
            print(f"--> DB Search empty. Falling back to INTERNET SEARCH.")
            web_context = web_search_direct(query)
            final_prompt = PromptTemplate.from_template(
                "Answer the user's question based on the following information from the internet.\n\n"
                "Internet Context: {context}\n\n"
                "User Question: {query}\n"
            )
            return llm.invoke(final_prompt.format(context=web_context, query=query)).content

        seen_contents = set()
        unique_contents = []
        for d in docs:
            content = d.get("content", "")
            if content and content not in seen_contents:
                seen_contents.add(content)
                unique_contents.append(content)

        context = "\n\n---\n\n".join(unique_contents)
        final_prompt = PromptTemplate.from_template(
            "Answer the user's question based on the following internal company knowledge base context.\n\n"
            "Context: {context}\n\n"
            "User Question: {query}\n"
        )
        return llm.invoke(final_prompt.format(context=context, query=query)).content

if __name__ == "__main__":
    test_query = "Привет, расскажи о себе"
    print(f"\n--- Testing Query: {test_query} ---")
    response = ask_oracle(test_query)
    print("Agent Response:\n", response)

if __name__ == "__main__":
    test_query_db = "Объясни, что такое RAG-система, кратко."
    print(f"\n--- Testing DB Search via Agent: {test_query_db} ---")
    response = ask_oracle(test_query_db)
    print("Agent Response:\n", response)

if __name__ == "__main__":
    test_query_web = "Какая сейчас погода в Москве?"
    print(f"\n--- Testing Web Search via Agent: {test_query_web} ---")
    response = ask_oracle(test_query_web)
    print("Agent Response:\n", response)
