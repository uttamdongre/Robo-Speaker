from utils import load_json, save_json


SEARCH_FILE = "search_history.json"


def add_search(keyword):

    history = load_json(SEARCH_FILE)

    if keyword in history:
        history.remove(keyword)

    history.insert(0, keyword)

    history = history[:20]

    save_json(SEARCH_FILE, history)


def show_search_history():

    history = load_json(SEARCH_FILE)

    if not history:
        print("\nNo Search History")
        return

    print("\n===== SEARCH HISTORY =====\n")

    for i, keyword in enumerate(history, start=1):
        print(f"{i}. {keyword}")
