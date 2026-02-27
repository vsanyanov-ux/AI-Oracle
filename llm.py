import os
from dotenv import load_dotenv
from langchain_gigachat import GigaChatLLM, ChatGigaChat
from gigachat import GigaChat

load_dotenv()

giga = GigaChat(credentials=os.getenv("GIGACHAT_CREDENTIALS"), scope=os.getenv("GIGACHAT_SCOPE"))

llm = ChatGigaChat(giga_chat=giga)  # Или GigaChatLLM(giga_chat=giga)

