# gigachat_test.py
import os
from dotenv import load_dotenv
from gigachat import GigaChat

load_dotenv()

client = GigaChat(
    credentials=os.getenv("GIGACHAT_CREDENTIALS"),
    scope=os.getenv("GIGACHAT_SCOPE"),
    verify_ssl_certs=False,  # важно
)

r = client.chat("Привет! Просто повтори слово ПОНЯТНО.")
print(r.choices[0].message.content)
