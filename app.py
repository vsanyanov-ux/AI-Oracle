import os
from dotenv import load_dotenv
from supabase import create_client, Client
from sentence_transformers import SentenceTransformer
from langchain_classic.chains import RetrievalQA
from llm import llm

chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(),
)

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

def ask_oracle(query: str, top_n: int = 3) -> str:
    docs = search(query, match_count=top_n)
    if not docs:
        return "Судя по базе знаний, я не нашёл ничего по этому запросу."

    seen_contents = set()
    unique_contents = []
    for d in docs:
        content = d.get("content", "")
        if content and content not in seen_contents:
            seen_contents.add(content)
            unique_contents.append(content)

    context = "\n\n---\n\n".join(unique_contents)

    return f"Судя по базе знаний, вот что нашёл:\n\n{context}"

if __name__ == "__main__":
    test_query = "Привет, расскажи о себе"
    response = llm.invoke(test_query)
    print(response)

if __name__ == "__main__":
    resp = llm.invoke("Коротко представься одним предложением.")
    print(resp)

 
  




