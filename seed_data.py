from sentence_transformers import SentenceTransformer
from supabase import create_client
from dotenv import load_dotenv
import os

# Загрузка .env (если используешь файл .env)
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

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

