from settings_manager import settings_menu
from pdf_reader import read_pdf
from stats_manager import show_statistics
from analytics_manager import analytics_menu
from export_manager import export_menu
from dashboard_manager import dashboard_menu


def text_mode():

    print("\nText Mode")

    print("Type 'exit' to return to menu")
    print("Type 'pause' to pause audio")
    print("Type 'resume' to resume audio")
    print("Type 'stop' to stop audio")

    while True:
        text = input("\nEnter text: ")

        command = text.lower().strip()

        if command == "exit":
            break

        elif command == "pause":
            pause_audio()

        elif command == "resume":
            resume_audio()

        elif command == "stop":
            stop_audio()

        else:
            speak(text)


def audio_controls():

    while True:
        print("\nAudio Controls")

        print("1. Pause")

        print("2. Resume")

        print("3. Stop")

        print("4. Back")

        choice = input("\nChoose: ")

        if choice == "1":
            pause_audio()

        elif choice == "2":
            resume_audio()

        elif choice == "3":
            stop_audio()

        elif choice == "4":
            break

        else:
            print("Invalid Choice")


def main():

    while True:
        print("\n===== ROBO SPEAKER =====")
        print("1. Speak Text")
        print("2. Read PDF")
        print("3. Settings")
        print("4. Statistics")
        print("5. Analytics")
        print("6. Dashboard")
        print("7. Export Data")
        print("8. Audio Controls")
        print("9. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            text_mode()

        elif choice == "2":
            read_pdf()

        elif choice == "3":
            settings_menu()

        elif choice == "4":
            show_statistics()

        elif choice == "5":
            analytics_menu()

        elif choice == "6":
            dashboard_menu()

        elif choice == "7":
            export_menu()

        elif choice == "8":
            audio_controls()

        elif choice == "9":
            stop_audio()

            speak_sapi("Bye Bye Friend")

            print("Goodbye!")

            break

        else:
            print("Invalid Choice")


if __name__ == "__main__":
    main()
