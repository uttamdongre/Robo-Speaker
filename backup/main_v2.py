import win32com.client
from PyPDF2 import PdfReader
import json
import os

# -----------------------------
# SPEECH ENGINE
# -----------------------------
speaker = win32com.client.Dispatch("SAPI.SpVoice")


def speak(text):
    if not text or not text.strip():
        return

    print(f"\nSpeaking: {text[:60]}...")
    speaker.Speak(text)


# -----------------------------
# PROGRESS FUNCTIONS
# -----------------------------
def load_progress():
    if os.path.exists("progress.json"):
        try:
            with open("progress.json", "r") as file:
                return json.load(file)
        except:
            return {}

    return {}


def save_progress(data):
    with open("progress.json", "w") as file:
        json.dump(data, file, indent=4)


# -----------------------------
# PDF READER
# -----------------------------
def read_pdf():

    pdf_path = input("\nEnter PDF path: ").strip()

    try:
        reader = PdfReader(pdf_path)
    except Exception as e:
        print("\nError opening PDF:", e)
        return

    total_pages = len(reader.pages)

    progress = load_progress()

    current_page = 1

    if pdf_path in progress:
        last_page = progress[pdf_path]

        resume = input(f"\nResume from page {last_page}? (y/n): ").lower()

        if resume == "y":
            current_page = last_page

    print("\nChoose Reading Mode")
    print("1. Continuous Reading")
    print("2. Interactive Reading")

    mode = input("Enter choice: ")

    # ==================================
    # CONTINUOUS MODE
    # ==================================
    if mode == "1":
        for page_no in range(current_page - 1, total_pages):
            print(f"\nReading Page {page_no + 1}/{total_pages}")

            text = reader.pages[page_no].extract_text()

            if text:
                speak(text)

            progress[pdf_path] = page_no + 1
            save_progress(progress)

        print("\nPDF Completed")

    # ==================================
    # INTERACTIVE MODE
    # ==================================
    elif mode == "2":
        while True:
            page = reader.pages[current_page - 1]

            text = page.extract_text()

            print(f"\nReading Page {current_page}/{total_pages}")

            if text:
                speak(text)

            progress[pdf_path] = current_page
            save_progress(progress)

            print("\nCommands")
            print("N = Next Page")
            print("B = Previous Page")
            print("J = Jump To Page")
            print("R = Replay Page")
            print("E = Exit")

            command = input("\nEnter command: ").lower()

            if command == "n":
                if current_page < total_pages:
                    current_page += 1
                else:
                    print("Already at last page")

            elif command == "b":
                if current_page > 1:
                    current_page -= 1
                else:
                    print("Already at first page")

            elif command == "j":
                try:
                    page_num = int(input(f"Enter page number (1-{total_pages}): "))

                    if 1 <= page_num <= total_pages:
                        current_page = page_num
                    else:
                        print("Invalid page")

                except ValueError:
                    print("Invalid number")

            elif command == "r":
                pass

            elif command == "e":
                print("\nProgress Saved")
                break

            else:
                print("Invalid command")

    else:
        print("Invalid mode selected")


# -----------------------------
# MAIN MENU
# -----------------------------
while True:
    print("\n===== ROBO SPEAKER =====")
    print("1. Speak Text")
    print("2. Read PDF")
    print("3. Exit")

    choice = input("\nEnter your choice: ")

    # -------------------------
    # TEXT MODE
    # -------------------------
    if choice == "1":
        print("\nText Mode")
        print("Type 'exit' to return to menu")

        while True:
            text = input("\nEnter text: ")

            if text.lower() == "exit":
                break

            speak(text)

    # -------------------------
    # PDF MODE
    # -------------------------
    elif choice == "2":
        read_pdf()

    # -------------------------
    # EXIT
    # -------------------------
    elif choice == "3":
        speak("Bye Bye Friend")

        print("Goodbye!")
        break

    else:
        print("Invalid choice")
