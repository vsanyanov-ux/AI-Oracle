#import os
#from dotenv import load_dotenv
#from supabase import create_client, Client
#from sentence_transformers import SentenceTransformer

#load_dotenv()

#SUPABASE_URL = os.getenv("SUPABASE_URL")
#SUPABASE_KEY = os.getenv("SUPABASE_KEY")

from supabase import create_client, Client
from sentence_transformers import SentenceTransformer

SUPABASE_URL = "https://ohpjeofoqlqccocqlpfy.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9ocGplb2ZvcWxxY2NvY3FscGZ5Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MjA0OTY3MiwiZXhwIjoyMDg3NjI1NjcyfQ.kaFZwFrityd-MPbzIpcGlP2QZN7IyhCffpihZ3plYSg"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


# Локальная модель эмбеддингов (можно поменять на другую)
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def embed(text: str) -> list[float]:
    vec = model.encode(text)
    return vec.tolist()


def seed_docs():
    docs = [
        {
            "title": "Общий обзор автоматизации с ИИ",
            "content": "Искусственный интеллект в автоматизации бизнес-процессов позволяет компаниям сократить рутинные операции на 70-80%. Нейронные сети обучаются на исторических данных и начинают самостоятельно принимать решения в типовых ситуациях.",
            "category": "overview",
            "topic": "general_automation",
            "complexity": "beginner",
        },
        {
            "title": "Чат-боты для клиентского сервиса",
            "content": "Внедрение ИИ-ассистентов для обработки клиентских запросов снижает нагрузку на службу поддержки в 3-5 раз. Чат-боты на основе больших языковых моделей понимают контекст диалога и доступны 24/7.",
            "category": "customer_service",
            "topic": "chatbots",
            "complexity": "beginner",
        },
        {
            "title": "RPA и интеллектуальная автоматизация",
            "content": "RPA в сочетании с машинным обучением создает интеллектуальную автоматизацию. Боты адаптируются к изменениям в интерфейсах и самостоятельно обрабатывают исключения.",
            "category": "process",
            "topic": "rpa",
            "complexity": "intermediate",
        },
        {
            "title": "Предиктивная аналитика",
            "content": "Предиктивная аналитика на основе ИИ помогает компаниям прогнозировать спрос и оптимизировать запасы. Алгоритмы анализируют тренды и выдают рекомендации с точностью до 95%.",
            "category": "analytics",
            "topic": "prediction",
            "complexity": "intermediate",
        },
    ]

    rows = []
    for doc in docs:
        print(f"Embedding: {doc['title']}")
        emb = embed(doc["content"])
        rows.append(
            {
                "title": doc["title"],
                "content": doc["content"],
                "category": doc["category"],
                "topic": doc["topic"],
                "complexity": doc["complexity"],
                "embedding": emb,
            }
        )

    print("Inserting batch...")
    supabase.table("docs").insert(rows).execute()
    print("✅ Docs seeded.")



if __name__ == "__main__":
    seed_docs()
