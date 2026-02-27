import os
from gigachat import GigaChat
from langchain_gigachat.chat_models import GigaChat as LangGigaChat

client = GigaChat(credentials=os.getenv("GIGACHAT_CREDENTIALS"), scope=os.getenv("GIGACHAT_SCOPE"))

llm = LangGigaChat(giga_chat=client)


