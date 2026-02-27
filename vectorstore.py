import os
from dotenv import load_dotenv
from supabase import create_client
from langchain_community.vectorstores import SupabaseVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# Важно: тот же embedding, что ты использовал при seed_documents
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = SupabaseVectorStore(
    client=supabase,
    table_name="documents",       # та же таблица
    query_name="match_docs", # имя RPC-функции в Supabase
    embedding=embeddings,
)
