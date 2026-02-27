import os
from dotenv import load_dotenv
from supabase import create_client, Client
from sentence_transformers import SentenceTransformer

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

    res = supabase.rpc(
        "match_docs",  # или "match_documents" — как у тебя в Supabase
        {
            "query_embedding": query_embedding,
            "match_threshold": match_threshold,
            "match_count": match_count,
        },
    ).execute()

    if res.error:
        print("Search error:", res.error)
        return []

    docs = res.data or []
    for d in docs:
        print("---")
        print("similarity:", d.get("similarity"))
        print("content:", d.get("content")[:200], "...")
    return docs
