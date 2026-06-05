from utils import load_json, save_json

COLLECTIONS_FILE = "collections.json"


def load_collections():
    return load_json(COLLECTIONS_FILE)


def save_collections(data):
    save_json(COLLECTIONS_FILE, data)


def add_favorite(pdf_path):

    data = load_collections()

    favorites = data.get("favorites", [])

    if pdf_path in favorites:
        print("Already in favorites")
        return

    favorites.append(pdf_path)

    data["favorites"] = favorites

    save_collections(data)

    print("Added to favorites")


def remove_favorite(pdf_path):

    data = load_collections()

    favorites = data.get("favorites", [])

    if pdf_path not in favorites:
        print("PDF not in favorites")
        return

    favorites.remove(pdf_path)

    data["favorites"] = favorites

    save_collections(data)

    print("Removed from favorites")


def view_favorites():

    data = load_collections()

    favorites = data.get("favorites", [])

    if not favorites:
        print("\nNo favorite PDFs found")
        return

    print("\n===== FAVORITE PDFs =====\n")

    for i, pdf in enumerate(favorites, start=1):
        print(f"{i}. {pdf}")


def assign_category(pdf_path):

    data = load_collections()

    category = input("\nCategory Name: ").strip()

    if not category:
        print("Category cannot be empty")
        return

    categories = data.get("categories", {})

    if category not in categories:
        categories[category] = []

    if pdf_path not in categories[category]:
        categories[category].append(pdf_path)

    data["categories"] = categories

    save_collections(data)

    print(f"Added to category: {category}")


def view_categories():

    data = load_collections()

    categories = data.get("categories", {})

    if not categories:
        print("\nNo categories found")
        return

    print("\n===== CATEGORIES =====\n")

    for category, pdfs in categories.items():
        print(f"{category}")

        for pdf in pdfs:
            print(f"   - {pdf}")

        print()


def remove_from_category(pdf_path):

    data = load_collections()

    categories = data.get("categories", {})

    category = input("\nCategory Name: ").strip()

    if category not in categories:
        print("Category not found")
        return

    if pdf_path in categories[category]:
        categories[category].remove(pdf_path)

        save_collections(data)

        print("Removed from category")
    else:
        print("PDF not found in category")


def add_to_reading_list(pdf_path):

    data = load_collections()

    reading_lists = data.get("reading_lists", {})

    list_name = input("\nReading List Name: ").strip()

    if not list_name:
        print("Reading list name cannot be empty")
        return

    if list_name not in reading_lists:
        reading_lists[list_name] = []

    if pdf_path not in reading_lists[list_name]:
        reading_lists[list_name].append(pdf_path)

    data["reading_lists"] = reading_lists

    save_collections(data)

    print(f"Added to reading list: {list_name}")


def view_reading_lists():

    data = load_collections()

    reading_lists = data.get("reading_lists", {})

    if not reading_lists:
        print("\nNo reading lists found")
        return

    print("\n===== READING LISTS =====\n")

    for list_name, pdfs in reading_lists.items():
        print(f"{list_name}")

        for pdf in pdfs:
            print(f"   - {pdf}")

        print()


def remove_from_reading_list(pdf_path):

    data = load_collections()

    reading_lists = data.get("reading_lists", {})

    list_name = input("\nReading List Name: ").strip()

    if list_name not in reading_lists:
        print("Reading list not found")
        return

    if pdf_path in reading_lists[list_name]:
        reading_lists[list_name].remove(pdf_path)

        save_collections(data)

        print("Removed from reading list")

    else:
        print("PDF not found in reading list")
