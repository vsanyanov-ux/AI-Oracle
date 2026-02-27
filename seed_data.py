from sentence_transformers import SentenceTransformer
from supabase import create_client
from dotenv import load_dotenv
import os
import textwrap

print("SUPABASE_URL =", SUPABASE_URL)

print(
    "SUPABASE_ANON_KEY (first 20 chars) =",
    SUPABASE_ANON_KEY[:20] if SUPABASE_ANON_KEY else None,
)

print("SUPABASE_ANON_KEY length =", len(SUPABASE_ANON_KEY) if SUPABASE_ANON_KEY else None)

# Загрузка .env (если используешь файл .env)
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL") or "https://ohpjeofoqlqccocqlpfy.supabase.co"
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY") or "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9ocGplb2ZvcWxxY2NvY3FscGZ5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzIwNDk2NzIsImV4cCI6MjA4NzYyNTY3Mn0.HwN58EL-TzEgxvWVf3u8jc7rla15lgCEWn4iMyhFYJ4"

supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def test_supabase():
    try:
        # простой запрос к существующей таблице
        res = supabase.table("documents").select("id").limit(1).execute()
        print("Supabase OK, got:", res.data)
    except Exception as e:
        print("Supabase ERROR:", e)

if __name__ == "__main__":
    test_supabase()



def seed_documents():
    docs = [
        {
            "content": "Автоматизация бизнес-процессов с помощью ИИ позволяет сократить ручной труд и снизить количество ошибок.",
            "metadata": {"topic": "automation", "lang": "ru"},
        },
        {
            "content": "RAG-система комбинирует поиск по базе знаний и генерацию ответа моделью, чтобы давать более точные ответы.",
            "metadata": {"topic": "rag", "lang": "ru"},
        },
    ]

    for doc in docs:
        print(f"Embedding: {doc['content'][:40]}...")
        emb = model.encode(doc["content"]).tolist()
        res = supabase.table("documents").insert(
            {
                "content": doc["content"],
                "metadata": doc["metadata"],
                "embedding": emb,
            }
        ).execute()
        print("Insert result:", res)

    print("✅ Документы засеяны")


if __name__ == "__main__":
    seed_documents()
