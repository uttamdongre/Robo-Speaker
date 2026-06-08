from datetime import datetime, timedelta
from utils import load_json, save_json

FILE = "sessions.json"


def load_sessions():
    return load_json(FILE)


def save_sessions(data):
    save_json(FILE, data)


def start_session():

    data = load_sessions()
    if data.get("session_start"):
        return

    data["session_start"] = datetime.now().isoformat()

    save_sessions(data)


def end_session():

    data = load_sessions()

    start = data.get("session_start")

    if not start:
        return

    start_time = datetime.fromisoformat(start)

    end_time = datetime.now()

    duration = int((end_time - start_time).total_seconds())

    sessions = data.get("sessions", [])

    sessions.append(
        {
            "date": end_time.strftime("%Y-%m-%d"),
            "duration": duration,
        }
    )

    data["sessions"] = sessions

    data["session_start"] = None

    save_sessions(data)


def show_session_stats():

    data = load_sessions()

    sessions = data.get(
        "sessions",
        [],
    )

    if not sessions:
        print("\nNo reading sessions found")

        return

    total_seconds = sum(s["duration"] for s in sessions)

    average_seconds = total_seconds // len(sessions)

    longest = max(s["duration"] for s in sessions)

    today = datetime.now().strftime("%Y-%m-%d")

    week_start = datetime.now() - timedelta(days=7)

    today_seconds = 0

    week_seconds = 0

    for session in sessions:
        session_date = datetime.strptime(
            session["date"],
            "%Y-%m-%d",
        )

        if session["date"] == today:
            today_seconds += session["duration"]

        if session_date >= week_start:
            week_seconds += session["duration"]

    print("\n===== READING SESSIONS =====")

    print(f"Total Sessions : {len(sessions)}")

    print(f"Reading Today  : {today_seconds // 60} min")

    print(f"Reading Week   : {week_seconds // 60} min")

    print(f"Average Session: {average_seconds // 60} min")

    print(f"Longest Session: {longest // 60} min")


def get_session_summary():

    data = load_sessions()

    sessions = data.get(
        "sessions",
        [],
    )

    if not sessions:
        return {
            "total_sessions": 0,
            "total_minutes": 0,
            "longest_minutes": 0,
        }

    total_seconds = sum(s["duration"] for s in sessions)

    longest = max(s["duration"] for s in sessions)

    return {
        "total_sessions": len(sessions),
        "total_minutes": total_seconds // 60,
        "longest_minutes": longest // 60,
    }
