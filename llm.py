# llm.py
import os
from dotenv import load_dotenv
from langchain_gigachat.chat_models import GigaChat
from gigachat import GigaChat as GigaChatClient

load_dotenv()

client = GigaChatClient(
    credentials=os.getenv("GIGACHAT_CREDENTIALS"),
    scope=os.getenv("GIGACHAT_SCOPE"),
    verify_ssl_certs=False  # Решение SSL-проблемы
)

llm = GigaChat(giga_chat=client)

