from app import ask_oracle

if __name__ == "__main__":
    print("Мини‑оракул. Введи вопрос (exit для выхода).")
    while True:
        q = input("\nВопрос: ").strip()
        if q.lower() in ("exit", "quit"):
            break
        print("\nОтвет оракула:\n")
        print(ask_oracle(q))
