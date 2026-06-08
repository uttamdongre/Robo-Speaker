from utils import load_json, save_json

FILE = "search_analytics.json"


def load_search_data():
    return load_json(FILE)


def save_search_data(data):
    save_json(FILE, data)


def increment_search(keyword):

    data = load_search_data()

    data["total_searches"] = data.get("total_searches", 0) + 1

    searches = data.get("top_searches", {})

    searches[keyword] = searches.get(keyword, 0) + 1

    data["top_searches"] = searches

    save_search_data(data)


def show_search_stats():

    data = load_search_data()

    print("\n===== SEARCH ANALYTICS =====")

    print(f"Total Searches : {data.get('total_searches', 0)}")

    print("\nTop Searches:")

    searches = data.get("top_searches", {})

    if not searches:
        print("No search data available")
        return

    sorted_searches = sorted(searches.items(), key=lambda x: x[1], reverse=True)

    for keyword, count in sorted_searches[:10]:
        print(f"{keyword} : {count}")


def add_search_new(keyword):
    increment_search(keyword)
