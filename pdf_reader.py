import os
from PyPDF2 import PdfReader

from speech import speak
from utils import load_json, save_json
from history_manager import add_recent_pdf, add_search_history
from stats_manager import increment_pdf_opened, increment_pages_read
from recent_manager import add_recent, show_recent
from search_manager import add_search, show_search_history
from notes_manager import add_note, view_notes, edit_note, delete_note
from collections_manager import (
    add_favorite,
    remove_favorite,
    view_favorites,
    assign_category,
    view_categories,
    remove_from_category,
    add_to_reading_list,
    view_reading_lists,
    remove_from_reading_list,
)
from analytics_manager import (
    load_analytics,
    save_analytics,
    update_reading_streak,
)
from search_analytics_manager import add_search


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
    add_search_history(keyword)
    add_search(keyword)

    matches = []

    print("\nSearching...\n")

    for page_no in range(total_pages):
        text = reader.pages[page_no].extract_text()

        if text and keyword in text.lower():
            matches.append(
                {"page": page_no + 1, "preview": text[:150].replace("\n", " ")}
            )

    if not matches:
        print("No matches found")
        return None

    print(f"\nFound on {len(matches)} page(s):")

    for item in matches:
        print(f"\nPage {item['page']}")
        print(item["preview"])

    try:
        page = int(input("\nJump to page: "))
        for item in matches:
            if item["page"] == page:
                return page

    except:
        pass

    return None


def search_pdf_keyword(reader, total_pages, keyword):

    add_search_history(keyword)

    add_search(keyword)

    matches = []

    print(f"\nSearching for: {keyword}\n")

    for page_no in range(total_pages):
        text = reader.pages[page_no].extract_text()

        if text and keyword.lower() in text.lower():
            matches.append(
                {
                    "page": page_no + 1,
                    "preview": text[:150].replace("\n", " "),
                }
            )

    if not matches:
        print("No matches found")
        return None

    print(f"\nFound on {len(matches)} page(s):")

    for item in matches:
        print(f"\nPage {item['page']}")

        print(item["preview"])

    try:
        page = int(input("\nJump to page: "))

        for item in matches:
            if item["page"] == page:
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

    bookmarks[pdf_path].append(
        {
            "name": name,
            "page": current_page,
            "note": note,
        }
    )

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
            analytics = load_analytics()
            analytics["today_pages"] += 1
            save_analytics(analytics)

        progress[pdf_path] = {"last_page": page_no}

        save_progress(progress)

    print("\nPDF Completed")

    progress[pdf_path] = {"last_page": 1}
    save_progress(progress)


def normalize_command(command):

    command = command.lower().strip()

    replacements = {
        "next page": "next",
        "previous page": "back",
        "go back": "back",
        "show bookmarks": "list bookmarks",
        "view bookmarks": "list bookmarks",
        "add bookmark": "bookmark",
        "create bookmark": "bookmark",
        "show notes": "v",
        "view notes": "v",
        "add note": "t",
        "create note": "t",
        "exit reader": "exit",
        "quit reader": "exit",
    }

    return replacements.get(command, command)


def interactive_reading(reader, pdf_path, current_page, total_pages):

    progress = load_progress()

    while True:
        print(f"\nReading Page {current_page}/{total_pages}")

        text = reader.pages[current_page - 1].extract_text()

        if text:
            speak(text)

            increment_pages_read()

            analytics = load_analytics()

            analytics["today_pages"] += 1

            save_analytics(analytics)

        progress[pdf_path] = {"last_page": current_page}

        save_progress(progress)

        print("\nCommands")

        print("next")
        print("back")

        print("jump 25")
        print("go to page 25")

        print("search python")
        print("search for python")
        print("find python")

        print("bookmark")
        print("show bookmarks")

        print("add note")
        print("show notes")

        print("exit")

        command = input("\nEnter Command: ").lower().strip()

        command = normalize_command(command)

        # NEXT

        if command in [
            "n",
            "next",
        ]:
            if current_page < total_pages:
                current_page += 1

        # BACK

        elif command in [
            "b",
            "back",
            "previous",
        ]:
            if current_page > 1:
                current_page -= 1

        # JUMP

        elif (
            command == "j"
            or command.startswith("jump")
            or command.startswith("go to page")
            or command.startswith("open page")
            or command.startswith("take me to page")
        ):
            page_number = None

            parts = command.split()

            for part in parts:
                if part.isdigit():
                    page_number = int(part)

                    break

            if page_number:
                if 1 <= page_number <= total_pages:
                    current_page = page_number

                    print(f"Jumped to page {page_number}")

            else:
                try:
                    page = int(input(f"Page (1-{total_pages}): "))

                    if 1 <= page <= total_pages:
                        current_page = page

                except:
                    pass

        # SEARCH

        elif (
            command.startswith("search")
            or command.startswith("find ")
            or command.startswith("look for ")
        ):
            keyword = None

            if command.startswith("search for "):
                keyword = command.replace(
                    "search for ",
                    "",
                    1,
                )

            elif command.startswith("search "):
                keyword = command.replace(
                    "search ",
                    "",
                    1,
                )

            elif command.startswith("find "):
                keyword = command.replace(
                    "find ",
                    "",
                    1,
                )

            elif command.startswith("look for "):
                keyword = command.replace(
                    "look for ",
                    "",
                    1,
                )

            if keyword:
                page = search_pdf_keyword(
                    reader,
                    total_pages,
                    keyword,
                )

            else:
                page = search_pdf(
                    reader,
                    total_pages,
                )

            if page:
                current_page = page

        # BOOKMARKS

        elif command in [
            "m",
            "bookmark",
        ]:
            add_bookmark(
                pdf_path,
                current_page,
            )

        elif command in [
            "l",
            "list bookmarks",
        ]:
            list_bookmarks(pdf_path)

        elif command in [
            "g",
            "go bookmark",
            "goto bookmark",
        ]:
            page = goto_bookmark(pdf_path)

            if page:
                current_page = page

        elif command in [
            "d",
            "delete bookmark",
        ]:
            delete_bookmark(pdf_path)

        # NOTES

        elif command in [
            "t",
            "add note",
            "create note",
        ]:
            add_note(
                pdf_path,
                current_page,
            )

        elif command in [
            "v",
            "show notes",
            "view notes",
        ]:
            view_notes(pdf_path)

        elif command == "u":
            edit_note(pdf_path)

        elif command == "x":
            delete_note(pdf_path)

        # SEARCH HISTORY

        elif command == "h":
            show_search_history()

        # REPLAY

        elif command == "r":
            continue

        # COLLECTIONS

        elif command == "f":
            add_favorite(pdf_path)

        elif command == "y":
            view_favorites()

        elif command == "z":
            remove_favorite(pdf_path)

        elif command == "c":
            assign_category(pdf_path)

        elif command == "k":
            view_categories()

        elif command == "q":
            remove_from_category(pdf_path)

        elif command == "p":
            add_to_reading_list(pdf_path)

        elif command == "w":
            view_reading_lists()

        elif command == "o":
            remove_from_reading_list(pdf_path)

        # EXIT

        elif command in [
            "e",
            "exit",
            "quit",
        ]:
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
        update_reading_streak()
        add_recent(pdf_path)
        add_recent_pdf(os.path.basename(pdf_path))
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
