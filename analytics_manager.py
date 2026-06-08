from datetime import datetime
from search_analytics_manager import show_search_stats
from utils import load_json, save_json

FILE = "analytics.json"


def load_analytics():
    return load_json(FILE)


def save_analytics(data):
    save_json(FILE, data)


def update_reading_streak():

    analytics = load_analytics()

    today = datetime.now().strftime("%Y-%m-%d")

    last_date = analytics.get("last_read_date", "")

    if last_date == today:
        return

    if last_date:
        last = datetime.strptime(last_date, "%Y-%m-%d")

        current = datetime.strptime(today, "%Y-%m-%d")

        diff = (current - last).days

        if diff == 1:
            analytics["current_streak"] += 1

        elif diff > 1:
            analytics["current_streak"] = 1

    else:
        analytics["current_streak"] = 1

    analytics["last_read_date"] = today

    if analytics["current_streak"] > analytics["longest_streak"]:
        analytics["longest_streak"] = analytics["current_streak"]

    save_analytics(analytics)


def set_daily_goal():

    analytics = load_analytics()

    try:
        goal = int(input("Daily Page Goal: "))

        analytics["daily_goal_pages"] = goal

        save_analytics(analytics)

        print("Goal Updated")

    except ValueError:
        print("Invalid Goal")


def show_goal_progress():

    analytics = load_analytics()

    pages = analytics.get("today_pages", 0)

    goal = analytics.get("daily_goal_pages", 20)

    print("\n===== DAILY GOAL =====")

    print(f"Pages Read : {pages}")
    print(f"Goal       : {goal}")

    if pages >= goal:
        print("Goal Achieved")
    else:
        print(f"Remaining  : {goal - pages}")


def show_analytics():

    analytics = load_analytics()

    print("\n===== READING ANALYTICS =====")

    print(f"Pages Read Today : {analytics.get('today_pages', 0)}")

    print(f"Current Streak   : {analytics.get('current_streak', 0)}")

    print(f"Longest Streak   : {analytics.get('longest_streak', 0)}")

    print(f"Daily Goal       : {analytics.get('daily_goal_pages', 20)}")


def analytics_menu():

    while True:
        print("\n===== ANALYTICS =====")

        print("1. View Analytics")
        print("2. Set Daily Goal")
        print("3. Goal Progress")
        print("4. Search Analytics")
        print("5. Back")

        choice = input("\nChoose: ")

        if choice == "1":
            show_analytics()

        elif choice == "2":
            set_daily_goal()

        elif choice == "3":
            show_goal_progress()

        elif choice == "4":
            show_search_stats()

        elif choice == "5":
            break

        else:
            print("Invalid Choice")
