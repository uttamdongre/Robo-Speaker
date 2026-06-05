from utils import load_json, save_json

RECENT_FILE = "recent_pdfs.json"


def load_recent():
    data = load_json(RECENT_FILE)

    if isinstance(data, list):
        return data

    return []


def save_recent(recent):
    save_json(RECENT_FILE, recent)


def add_recent(pdf_path):

    recent = load_recent()

    if pdf_path in recent:
        recent.remove(pdf_path)

    recent.insert(0, pdf_path)

    recent = recent[:10]

    save_recent(recent)


def show_recent():

    recent = load_recent()

    if not recent:
        print("\nNo recent PDFs found.")
        return None

    print("\n===== RECENT PDFs =====\n")

    for i, pdf in enumerate(recent, start=1):
        print(f"{i}. {pdf}")

    print("\n0. Browse PDF Library")

    try:
        choice = int(input("\nChoose PDF: "))

        if choice == 0:
            return None

        if 1 <= choice <= len(recent):
            return recent[choice - 1]

    except:
        pass

    return None
