from PyPDF2 import PdfReader

from speech import speak
from utils import load_json, save_json


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

        progress[pdf_path] = {"last_page": page_no}

        save_progress(progress)

    print("\nPDF Completed")


def interactive_reading(reader, pdf_path, current_page, total_pages):

    progress = load_progress()

    while True:
        print(f"\nReading Page {current_page}/{total_pages}")

        text = reader.pages[current_page - 1].extract_text()

        if text:
            speak(text)

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
                    print(f"DEBUG: Jumped to page {current_page}")
            except:
                pass

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
            print("Progress Saved")
            break


# -------------------------
# MAIN ENTRY
# -------------------------


def read_pdf():

    pdf_path = input("\nEnter PDF Path: ").strip()

    try:
        reader = PdfReader(pdf_path)

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
