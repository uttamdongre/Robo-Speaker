import os

from notes_manager import load_notes
from pdf_reader import load_bookmarks
from stats_manager import load_stats


EXPORT_FOLDER = "exports"


def ensure_export_folder():

    if not os.path.exists(EXPORT_FOLDER):
        os.makedirs(EXPORT_FOLDER)


def export_notes():

    ensure_export_folder()

    notes = load_notes()

    file_path = os.path.join(EXPORT_FOLDER, "notes_export.txt")

    with open(file_path, "w", encoding="utf-8") as file:
        file.write("ROBO SPEAKER NOTES EXPORT\n\n")

        for pdf, note_list in notes.items():
            file.write(f"PDF: {pdf}\n")

            file.write("-" * 40 + "\n")

            for note in note_list:
                file.write(f"Page: {note['page']}\n")

                file.write(f"Note: {note['note']}\n\n")

    print(f"\nNotes exported to:\n{file_path}")


def export_bookmarks():

    ensure_export_folder()

    bookmarks = load_bookmarks()

    file_path = os.path.join(EXPORT_FOLDER, "bookmarks_export.txt")

    with open(file_path, "w", encoding="utf-8") as file:
        file.write("ROBO SPEAKER BOOKMARK EXPORT\n\n")

        for pdf, bookmark_list in bookmarks.items():
            file.write(f"PDF: {pdf}\n")

            file.write("-" * 40 + "\n")

            for bookmark in bookmark_list:
                file.write(f"Name: {bookmark['name']}\n")

                file.write(f"Page: {bookmark['page']}\n")

                file.write(f"Note: {bookmark['note']}\n\n")

    print(f"\nBookmarks exported to:\n{file_path}")


def export_statistics():

    ensure_export_folder()

    stats = load_stats()

    file_path = os.path.join(EXPORT_FOLDER, "statistics_export.txt")

    with open(file_path, "w", encoding="utf-8") as file:
        file.write("ROBO SPEAKER STATISTICS\n\n")

        for key, value in stats.items():
            file.write(f"{key}: {value}\n")

    print(f"\nStatistics exported to:\n{file_path}")


def export_menu():

    while True:
        print("\n===== EXPORTS =====")

        print("1. Export Notes")
        print("2. Export Bookmarks")
        print("3. Export Statistics")
        print("4. Back")

        choice = input("\nChoose: ")

        if choice == "1":
            export_notes()

        elif choice == "2":
            export_bookmarks()

        elif choice == "3":
            export_statistics()

        elif choice == "4":
            break

        else:
            print("Invalid Choice")
