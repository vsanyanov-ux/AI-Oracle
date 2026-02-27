import os
from dotenv import load_dotenv

print("=== check_env.py started ===")

env_path = os.path.join(os.path.dirname(__file__), ".env")
print("Env path exists:", os.path.isfile(env_path), "->", env_path)

loaded = load_dotenv(dotenv_path=env_path)
print("load_dotenv result:", loaded)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

print("URL:", repr(SUPABASE_URL))
print("ANON KEY prefix:", repr((SUPABASE_ANON_KEY or "")[:40]))
print("ANON KEY length:", len(SUPABASE_ANON_KEY) if SUPABASE_ANON_KEY else None)

print("=== check_env.py finished ===")