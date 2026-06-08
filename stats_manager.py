from utils import load_json, save_json

STATS_FILE = "stats.json"


def load_stats():
    return load_json(STATS_FILE)


def save_stats(stats):
    save_json(STATS_FILE, stats)


def increment_pdf_opened(pdf_name):

    stats = load_stats()

    stats["total_pdfs_read"] = stats.get("total_pdfs_read", 0) + 1

    stats["reading_sessions"] = stats.get("reading_sessions", 0) + 1

    stats["last_pdf_opened"] = pdf_name

    pdf_counts = stats.get("pdf_open_counts", {})

    pdf_counts[pdf_name] = pdf_counts.get(pdf_name, 0) + 1

    stats["pdf_open_counts"] = pdf_counts

    save_stats(stats)


def increment_pages_read():

    stats = load_stats()

    stats["total_pages_read"] = stats.get("total_pages_read", 0) + 1

    save_stats(stats)


def show_statistics():

    stats = load_stats()

    print("\n===== READING STATISTICS =====\n")

    print(f"Total PDFs Read      : {stats.get('total_pdfs_read', 0)}")

    print(f"Total Pages Read     : {stats.get('total_pages_read', 0)}")

    print(f"Reading Sessions     : {stats.get('reading_sessions', 0)}")

    print(f"Last PDF Opened      : {stats.get('last_pdf_opened', 'None')}")

    pdf_counts = stats.get(
        "pdf_open_counts",
        {},
    )

    if pdf_counts:
        top_pdf = max(
            pdf_counts,
            key=pdf_counts.get,
        )

        print(f"Most Opened PDF      : {top_pdf}")
