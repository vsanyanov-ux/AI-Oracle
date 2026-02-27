# config.py - запускать первым!
import os
import ssl
import certifi
from dotenv import load_dotenv

load_dotenv()

# Глобальное отключение SSL для Windows/GigaChat
os.environ['CURL_CA_BUNDLE'] = ''
os.environ['REQUESTS_CA_BUNDLE'] = ''
ssl._create_default_https_context = ssl._create_unverified_context
