from app import search

if __name__ == "__main__":
    docs = search("автоматизация бизнес-процессов с помощью ИИ")
    print("Found:", len(docs))
