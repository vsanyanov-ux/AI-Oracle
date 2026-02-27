import os
from dotenv import load_dotenv
from gigachat import GigaChat
from langchain_gigachat.chat_models import GigaChat as LangGigaChat

load_dotenv()

client = GigaChat(
    credentials=os.getenv("GIGACHAT_CREDENTIALS"),
    scope=os.getenv("GIGACHAT_SCOPE"),
    verify_ssl_certs=False,
)

llm = LangGigaChat(giga_chat=client)



