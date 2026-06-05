import os
from PyPDF2 import PdfReader

from speech import speak
from utils import load_json, save_json

from stats_manager import increment_pdf_opened, increment_pages_read
from recent_manager import add_recent, show_recent
from search_manager import add_search, show_search_history


def select_pdf():

    pdf_folder = "pdfs"

    if not os.path.exists(pdf_folder):
        os.makedirs(pdf_folder)
        print("Created pdfs folder. Add PDFs and try again.")
        return None
    pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith(".pdf")]

    if not pdf_files:
        print("No PDFs found in pdfs folder")
        return None

    print("\nAvailable PDFs\n")

    for i, pdf in enumerate(pdf_files, start=1):
        print(f"{i}. {pdf}")

    try:
        choice = int(input("\nSelect PDF: "))

        if 1 <= choice <= len(pdf_files):
            return os.path.join(pdf_folder, pdf_files[choice - 1])

    except:
        pass

    print("Invalid selection")
    return None


def search_pdf(reader, total_pages):

    keyword = input("\nSearch text: ").lower()
    add_search(keyword)

    matches = []

    print("\nSearching...\n")

    for page_no in range(total_pages):
        text = reader.pages[page_no].extract_text()

        if text and keyword in text.lower():
            matches.append(page_no + 1)

    if not matches:
        print("No matches found")
        return None

    print(f"\nFound on {len(matches)} page(s):")

    for page in matches:
        print(page)

    try:
        page = int(input("\nJump to page: "))

        if page in matches:
            return page

    except:
        pass

    return None


# -------------------------
# PROGRESS
# -------------------------


def load_progress():
    return load_json("progress.json")


def save_progress(progress):
    save_json("progress.json", progress)


# -------------------------
# BOOKMARKS
# -------------------------


def load_bookmarks():
    return load_json("bookmarks.json")


def save_bookmarks(bookmarks):
    save_json("bookmarks.json", bookmarks)


def add_bookmark(pdf_path, current_page):

    bookmarks = load_bookmarks()

    if pdf_path not in bookmarks:
        bookmarks[pdf_path] = []

    name = input("Bookmark Name: ")

    if not name.strip():
        print("Bookmark name cannot be empty")
        return
    note = input("Bookmark Note: ")

    if not os.name.strip():
        print("Bookmark name cannot be empty")
        return
    note = input("Bookmark Note: ")

    bookmarks[pdf_path].append({"name": name, "page": current_page, "note": note})

    save_bookmarks(bookmarks)

    print("Bookmark Saved")


def list_bookmarks(pdf_path):

    bookmarks = load_bookmarks()

    if pdf_path not in bookmarks:
        print("No bookmarks found")
        return

    print("\nBookmarks\n")

    for i, bookmark in enumerate(bookmarks[pdf_path], start=1):
        print(f"{i}. {bookmark['name']} (Page {bookmark['page']})")

        print(f"   Note: {bookmark['note']}")


def goto_bookmark(pdf_path):

    bookmarks = load_bookmarks()

    if pdf_path not in bookmarks:
        print("No bookmarks found")
        return None

    if len(bookmarks[pdf_path]) == 0:
        print("No bookmarks found")
        return None

    list_bookmarks(pdf_path)

    try:
        choice = int(input("\nSelect Bookmark Number: "))

        return bookmarks[pdf_path][choice - 1]["page"]

    except:
        print("Invalid Selection")
        return None


def delete_bookmark(pdf_path):

    bookmarks = load_bookmarks()

    if pdf_path not in bookmarks:
        print("No bookmarks found")
        return

    if len(bookmarks[pdf_path]) == 0:
        print("No bookmarks found")
        return

    list_bookmarks(pdf_path)

    try:
        choice = int(input("\nBookmark Number To Delete: "))

        deleted = bookmarks[pdf_path].pop(choice - 1)

        save_bookmarks(bookmarks)

        print(f"Deleted: {deleted['name']}")

    except:
        print("Invalid Selection")


# -------------------------
# READING MODES
# -------------------------


def continuous_reading(reader, pdf_path, current_page, total_pages):

    progress = load_progress()

    for page_no in range(current_page, total_pages + 1):
        print(f"\nReading Page {page_no}/{total_pages}")

        text = reader.pages[page_no - 1].extract_text()

        if text:
            speak(text)
            increment_pages_read()

        progress[pdf_path] = {"last_page": page_no}

        save_progress(progress)

    print("\nPDF Completed")

    progress[pdf_path] = {"last_page": 1}
    save_progress(progress)


def interactive_reading(reader, pdf_path, current_page, total_pages):

    progress = load_progress()

    while True:
        print(f"\nReading Page {current_page}/{total_pages}")

        text = reader.pages[current_page - 1].extract_text()

        if text:
            speak(text)
            increment_pages_read()

        progress[pdf_path] = {"last_page": current_page}

        save_progress(progress)

        print("\nCommands")
        print("N = Next")
        print("B = Back")
        print("J = Jump")
        print("R = Replay")
        print("M = Bookmark")
        print("L = List Bookmarks")
        print("G = Go To Bookmark")
        print("D = Delete Bookmark")
        print("S = Search")
        print("H = Search History")
        print("E = Exit")

        command = input("\nEnter Command: ").lower()

        if command == "n":
            if current_page < total_pages:
                current_page += 1

        elif command == "b":
            if current_page > 1:
                current_page -= 1

        elif command == "j":
            try:
                page = int(input(f"Page (1-{total_pages}): "))

                if 1 <= page <= total_pages:
                    current_page = page
                    print(f"Jumped to page {current_page}")
            except:
                pass

        elif command == "s":
            page = search_pdf(reader, total_pages)

            if page:
                current_page = page

        elif command == "h":
            show_search_history()

        elif command == "r":
            continue

        elif command == "m":
            add_bookmark(pdf_path, current_page)

        elif command == "l":
            list_bookmarks(pdf_path)

        elif command == "g":
            page = goto_bookmark(pdf_path)

            if page:
                current_page = page

        elif command == "d":
            delete_bookmark(pdf_path)

        elif command == "e":
            if current_page >= total_pages:
                progress[pdf_path] = {"last_page": 1}
            else:
                progress[pdf_path] = {"last_page": current_page}

            save_progress(progress)

            print("Progress Saved")
            break

        else:
            print("Invalid Command")


# -------------------------
# MAIN ENTRY
# -------------------------


def read_pdf():

    print("\n1. Recent PDFs")
    print("2. Browse PDF Library")

    choice = input("\nChoose: ")

    if choice == "1":
        pdf_path = show_recent()

        if not pdf_path:
            pdf_path = select_pdf()

    else:
        pdf_path = select_pdf()

    if not pdf_path:
        return

    try:
        reader = PdfReader(pdf_path)
        add_recent(pdf_path)
        increment_pdf_opened(os.path.basename(pdf_path))

    except Exception as e:
        print(f"\nUnable To Open PDF: {e}")

        return

    total_pages = len(reader.pages)

    progress = load_progress()

    current_page = 1

    if pdf_path in progress:
        resume = input(
            f"\nResume from page {progress[pdf_path]['last_page']}? (y/n): "
        ).lower()

        if resume == "y":
            current_page = progress[pdf_path]["last_page"]

    print("\nChoose Mode")
    print("1. Continuous Reading")
    print("2. Interactive Reading")

    mode = input("Enter Choice: ")

    if mode == "1":
        continuous_reading(reader, pdf_path, current_page, total_pages)

    elif mode == "2":
        interactive_reading(reader, pdf_path, current_page, total_pages)

    else:
        print("Invalid Choice")
