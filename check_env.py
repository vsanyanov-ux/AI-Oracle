import os
from dotenv import load_dotenv

print("=== check_env.py started ===")

env_path = os.path.join(os.path.dirname(__file__), ".env")
print("Env path exists:", os.path.isfile(env_path), "->", env_path)

loaded = load_dotenv(dotenv_path=env_path)
print("load_dotenv result:", loaded)

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_ANON_KEY")

print("URL:", repr(url))
print("KEY prefix:", repr((key or "")[:40]))
print("KEY length:", len(key) if key else None)

print("=== check_env.py finished ===")