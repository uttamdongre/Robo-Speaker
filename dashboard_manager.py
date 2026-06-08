from history_manager import (
    show_search_history,
    show_recent_pdfs,
)
from stats_manager import load_stats
from analytics_manager import load_analytics
from search_analytics_manager import load_search_data
from analytics_manager import show_analytics
from search_analytics_manager import show_search_stats
from session_manager import get_session_summary, load_sessions
from utils import load_json


def show_reading_insights():

    stats = load_stats()

    collections = load_json("collections.json")

    progress = load_json("progress.json")

    pdf_counts = stats.get(
        "pdf_open_counts",
        {},
    )
    completed = 0

    in_progress = 0

    not_started = 0

    print("\n===== READING INSIGHTS =====\n")

    if pdf_counts:
        most_opened = max(
            pdf_counts,
            key=pdf_counts.get,
        )

        least_opened = min(
            pdf_counts,
            key=pdf_counts.get,
        )

        print(f"Most Opened PDF  : {most_opened}")
        print(f"Least Opened PDF : {least_opened}")
    else:
        print("Most Opened PDF  : None")
        print("Least Opened PDF : None")

    for pdf_data in progress.values():
        last_page = pdf_data.get(
            "last_page",
            0,
        )

        total_pages = pdf_data.get(
            "total_pages",
            0,
        )

        if total_pages <= 0:
            continue

        percent = int((last_page / total_pages) * 100)

        if percent >= 100:
            completed += 1

        elif percent == 0:
            not_started += 1

        else:
            in_progress += 1

    total_tracked = completed + in_progress + not_started

    completion_rate = 0

    if total_tracked > 0:
        completion_rate = int((completed / total_tracked) * 100)

    print(f"Completed PDFs   : {completed}")
    print(f"In Progress PDFs : {in_progress}")
    print(f"Not Started PDFs : {not_started}")
    print(f"Completion Rate  : {completion_rate}%")

    print(f"Categories       : {len(collections.get('categories', {}))}")

    print(f"Reading Lists    : {len(collections.get('reading_lists', {}))}")


def show_reading_trends():

    analytics = load_analytics()

    sessions_data = load_sessions()

    sessions = sessions_data.get(
        "sessions",
        [],
    )

    total_sessions = len(sessions)

    pages_today = analytics.get(
        "today_pages",
        0,
    )

    avg_pages = 0

    if total_sessions > 0:
        avg_pages = round(
            pages_today / total_sessions,
            2,
        )

    day_counts = {}

    for session in sessions:
        day = session.get(
            "date",
            "Unknown",
        )

        day_counts[day] = day_counts.get(day, 0) + 1

    most_active_day = "None"

    if day_counts:
        most_active_day = max(
            day_counts,
            key=day_counts.get,
        )

    print("\n===== READING TRENDS =====\n")

    print(f"Pages Read Today       : {pages_today}")

    print(f"Reading Sessions       : {total_sessions}")

    print(f"Average Pages/Session  : {avg_pages}")

    print(f"Most Active Day        : {most_active_day}")

    print(f"Current Streak         : {analytics.get('current_streak', 0)}")

    print(f"Longest Streak         : {analytics.get('longest_streak', 0)}")


def dashboard_menu():

    while True:
        print("\n===== DASHBOARD =====")

        print("1. Recent PDFs")
        print("2. Recent Searches")
        print("3. Reading Analytics")
        print("4. Search Analytics")
        print("5. Activity Summary")
        print("6. Reading Insights")
        print("7. Reading Trends")
        print("8. Back")

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
            show_activity_summary()

        elif choice == "6":
            show_reading_insights()

        elif choice == "7":
            show_reading_trends()
        elif choice == "8":
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
