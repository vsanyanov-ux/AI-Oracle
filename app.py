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
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9ocGplb2ZvcWxxY2NvY3FscGZ5Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MjA0OTY3MiwiZXhwIjoyMDg3NjI1NjcyfQ.kaFZwFrityd-MPbzIpcGlP2QZN7IyhCffpihZ3plYSg"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


# Локальная модель эмбеддингов (можно поменять на другую)
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def embed(text: str) -> list[float]:
    vec = model.encode(text)
    return vec.tolist()
