import os

from utils import load_json
from history_manager import show_recent_pdfs
from collections_manager import view_favorites, view_categories


def show_library():

    pdf_folder = "pdfs"

    if not os.path.exists(pdf_folder):
        print("PDF folder not found")
        return

    pdfs = sorted([f for f in os.listdir(pdf_folder) if f.lower().endswith(".pdf")])

    if not pdfs:
        print("No PDFs found")
        return

    progress = load_json("progress.json")

    collections = load_json("collections.json")

    favorites = collections.get(
        "favorites",
        [],
    )

    categories = collections.get(
        "categories",
        {},
    )

    stats = load_json("stats.json")

    pdf_counts = stats.get("pdf_open_counts", {})

    favorite_count = 0

    in_progress_count = 0

    not_started_count = 0

    completed_count = 0

    for pdf in pdfs:
        full_path = os.path.join(
            pdf_folder,
            pdf,
        )

        if full_path in favorites:
            favorite_count += 1

    print("\n===== PDF LIBRARY =====\n")

    for pdf in pdfs:
        full_path = os.path.join(
            pdf_folder,
            pdf,
        )

        last_page = 1

        if full_path in progress:
            last_page = progress[full_path].get(
                "last_page",
                1,
            )

        is_favorite = "No"

        if full_path in favorites:
            is_favorite = "Yes"

        category = "None"

        for cat, files in categories.items():
            if full_path in files:
                category = cat

                break

        reading_list = "None"

        lists = collections.get(
            "reading_lists",
            {},
        )

        for list_name, files in lists.items():
            if full_path in files:
                reading_list = list_name

                break

        open_count = pdf_counts.get(
            pdf,
            0,
        )

        progress_percent = 0

        pdf_progress = progress.get(
            full_path,
            {},
        )

        total_pages = pdf_progress.get(
            "total_pages",
            0,
        )

        if total_pages > 0:
            progress_percent = int((last_page / total_pages) * 100)

        if progress_percent == 0:
            status = "Not Started"
            not_started_count += 1

        elif progress_percent >= 100:
            status = "Completed"
            completed_count += 1

        else:
            status = "In Progress"
            in_progress_count += 1

        print(pdf)

        print(f"Last Page Read : {last_page}")

        print(f"Favorite       : {is_favorite}")

        print(f"Category       : {category}")

        print(f"Reading List   : {reading_list}")

        print(f"Times Opened   : {open_count}")

        print(f"Status         : {status}")

        print(f"Progress       : {progress_percent}% ({last_page}/{total_pages} pages)")

        print("-" * 40)

    category_count = len(
        collections.get(
            "categories",
            {},
        )
    )
    reading_list_count = len(
        collections.get(
            "reading_lists",
            {},
        )
    )
    print("\n===== LIBRARY SUMMARY =====")

    print(f"Total PDFs      : {len(pdfs)}")

    print(f"Favorites       : {favorite_count}")

    print(f"Categories      : {category_count}")

    print(f"Reading Lists   : {reading_list_count}")

    print(f"In Progress     : {in_progress_count}")

    print(f"Not Started     : {not_started_count}")

    print(f"Completed       : {completed_count}")


def search_library():

    pdf_folder = "pdfs"

    if not os.path.exists(pdf_folder):
        print("PDF folder not found")
        return

    pdfs = sorted([f for f in os.listdir(pdf_folder) if f.lower().endswith(".pdf")])

    keyword = input("\nSearch Library: ").lower()

    matches = []

    for pdf in pdfs:
        if keyword in pdf.lower():
            matches.append(pdf)

    print("\n===== RESULTS =====\n")

    if not matches:
        print("No PDFs found")

        return

    for pdf in matches:
        print(pdf)


def show_top_pdfs():

    stats = load_json("stats.json")

    pdf_counts = stats.get("pdf_open_counts", {})

    print("\n===== TOP PDFs =====\n")

    if not pdf_counts:
        print("No reading data available")

        return

    ranking = sorted(
        pdf_counts.items(),
        key=lambda x: x[1],
        reverse=True,
    )

    for i, (pdf, count) in enumerate(
        ranking[:5],
        start=1,
    ):
        print(f"{i}. {pdf} ({count} opens)")


def library_health_check():

    collections = load_json("collections.json")

    issues = []

    favorites = collections.get(
        "favorites",
        [],
    )

    for pdf in favorites:
        if not os.path.exists(pdf):
            issues.append(f"Missing Favorite: {pdf}")

    categories = collections.get(
        "categories",
        {},
    )

    for category, files in categories.items():
        for pdf in files:
            if not os.path.exists(pdf):
                issues.append(f"Missing Category PDF: {pdf}")

    reading_lists = collections.get(
        "reading_lists",
        {},
    )

    for list_name, files in reading_lists.items():
        for pdf in files:
            if not os.path.exists(pdf):
                issues.append(f"Missing Reading List PDF: {pdf}")

    print("\n===== LIBRARY HEALTH =====\n")

    if not issues:
        print("No issues found")

        return

    for issue in issues:
        print(issue)

    print(f"\nFound {len(issues)} issue(s)")


def library_menu():

    while True:
        print("\n===== LIBRARY =====")

        print("1. View Library")

        print("2. Search Library")

        print("3. Top PDFs")

        print("4. Recently Opened")

        print("5. Favorites")

        print("6. Categories")

        print("7. Reading Insights")

        print("8. Library Health Check")

        print("9. Back")

        choice = input("\nChoose: ")

        if choice == "1":
            show_library()

        elif choice == "2":
            search_library()

        elif choice == "3":
            show_top_pdfs()

        elif choice == "4":
            show_recent_pdfs()

        elif choice == "5":
            view_favorites()

        elif choice == "6":
            view_categories()

        elif choice == "7":
            reading_insights_menu()

        elif choice == "8":
            library_health_check()
        elif choice == "9":
            break

        else:
            print("Invalid Choice")


def reading_insights_menu():

    while True:
        print("\n===== READING INSIGHTS =====")

        print("1. Unread PDFs")

        print("2. Category Statistics")

        print("3. Back")

        choice = input("\nChoose: ")

        if choice == "1":
            show_unread_pdfs()

        elif choice == "2":
            show_category_stats()

        elif choice == "3":
            break

        else:
            print("Invalid Choice")


def show_unread_pdfs():

    pdf_folder = "pdfs"

    pdfs = sorted([f for f in os.listdir(pdf_folder) if f.lower().endswith(".pdf")])

    stats = load_json("stats.json")

    pdf_counts = stats.get(
        "pdf_open_counts",
        {},
    )

    print("\n===== UNREAD PDFS =====\n")

    found = False

    for pdf in pdfs:
        if pdf_counts.get(pdf, 0) == 0:
            found = True

            print(pdf)

    if not found:
        print("All PDFs have been opened")


def show_category_stats():

    data = load_json("collections.json")

    categories = data.get(
        "categories",
        {},
    )

    print("\n===== CATEGORY STATISTICS =====\n")

    if not categories:
        print("No categories found")

        return

    for category, pdfs in categories.items():
        print(f"{category} : {len(pdfs)} PDF(s)")
