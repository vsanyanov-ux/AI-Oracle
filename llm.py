import os
from dotenv import load_dotenv
from langchain_community.chat_models import GigaChat  # ВАЖНО: из langchain_community, не langchain_gigachat

load_dotenv()

llm = GigaChat(
    credentials=os.getenv("GIGACHAT_CREDENTIALS"),
    scope=os.getenv("GIGACHAT_SCOPE"),
    verify_ssl_certs=False,      # уже использовали в тесте
)




