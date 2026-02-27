import os
from dotenv import load_dotenv
from gigachat import GigaChat

load_dotenv()  # Загружает .env автоматически

credentials = os.getenv("GIGACHAT_CREDENTIALS")
scope = os.getenv("GIGACHAT_SCOPE")

giga = GigaChat(credentials=credentials, scope=scope)
