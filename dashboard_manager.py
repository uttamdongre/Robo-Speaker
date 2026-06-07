from history_manager import (
    show_search_history,
    show_recent_pdfs,
)
from stats_manager import load_stats
from analytics_manager import load_analytics
from search_analytics_manager import load_search_data
from analytics_manager import show_analytics
from search_analytics_manager import show_search_stats
from session_manager import show_session_stats, get_session_summary


def dashboard_menu():

    while True:
        print("\n===== DASHBOARD =====")

        print("1. Recent PDFs")
        print("2. Recent Searches")
        print("3. Reading Analytics")
        print("4. Search Analytics")
        print("5. Reading Sessions")
        print("6. Activity Summary")
        print("7. Back")

        choice = input("\nChoose: ")

        if choice == "1":
            show_recent_pdfs()

        elif choice == "2":
            show_search_history()

        elif choice == "3":
            show_analytics()

        elif choice == "4":
            show_search_stats()

        elif choice == "5":
            show_session_stats()

        elif choice == "6":
            show_activity_summary()

        elif choice == "7":
            break

        else:
            print("Invalid Choice")


def show_activity_summary():

    stats = load_stats()

    analytics = load_analytics()

    search_data = load_search_data()

    session_data = get_session_summary()

    print("\n===== ACTIVITY SUMMARY =====\n")

    print(f"Pages Read Today : {analytics.get('today_pages', 0)}")

    print(f"Current Streak   : {analytics.get('current_streak', 0)}")

    print(f"Longest Streak   : {analytics.get('longest_streak', 0)}")

    print(f"Reading Sessions : {session_data['total_sessions']}")

    print(f"Reading Minutes  : {session_data['total_minutes']}")

    print(f"Longest Session  : {session_data['longest_minutes']} min")

    print(f"Total Searches   : {search_data.get('total_searches', 0)}")

    searches = search_data.get("top_searches", {})

    if searches:
        top_search = max(searches, key=searches.get)

        print(f"Most Searched    : {top_search}")

    pdf_counts = stats.get("pdf_open_counts", {})

    if pdf_counts:
        top_pdf = max(pdf_counts, key=pdf_counts.get)

        print(f"Most Opened PDF  : {top_pdf}")
