from utils import load_json, save_json

FILE = "search_history.json"


def load_history():
    return load_json(FILE)


def save_history(data):
    save_json(FILE, data)


def add_search_history(keyword):

    history = load_history()

    history.insert(0, keyword)

    history = history[:20]

    save_history(history)


def show_search_history():

    history = load_history()

    print("\n===== SEARCH HISTORY =====")

    if not history:
        print("No searches found")
        return

    for i, item in enumerate(history, start=1):
        print(f"{i}. {item}")


PDF_FILE = "recent_pdfs.json"


def load_recent_pdfs():
    return load_json(PDF_FILE)


def save_recent_pdfs(data):
    save_json(PDF_FILE, data)


def add_recent_pdf(pdf_name):

    data = load_recent_pdfs()

    data.insert(0, pdf_name)

    data = data[:10]

    save_recent_pdfs(data)


def show_recent_pdfs():

    data = load_recent_pdfs()

    print("\n===== RECENT PDFS =====")

    if not data:
        print("No PDFs opened")
        return

    for i, item in enumerate(data, start=1):
        print(f"{i}. {item}")
