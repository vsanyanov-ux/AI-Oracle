from sentence_transformers import SentenceTransformer
from supabase import create_client
import os

model = SentenceTransformer("all-MiniLM-L6-v2")

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

def seed_documents():
    docs = [
        {
            "content": "Автоматизация бизнес-процессов с помощью ИИ позволяет сократить ручной труд и снизить количество ошибок.",
            "metadata": {"topic": "automation", "lang": "ru"}
        },
        {
            "content": "RAG-система комбинирует поиск по базе знаний и генерацию ответа моделью, чтобы давать более точные ответы.",
            "metadata": {"topic": "rag", "lang": "ru"}
        },
    ]

    for doc in docs:
        emb = model.encode(doc["content"]).tolist()  # это будет список из 384 чисел
        supabase.table("documents").insert({
            "content": doc["content"],
            "metadata": doc["metadata"],
            "embedding": emb
        }).execute()

if __name__ == "__main__":
    seed_documents()
    print("✅ Документы засеяны")
