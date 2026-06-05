from settings_manager import settings_menu
from speech import speak
from pdf_reader import read_pdf


def text_mode():

    print("\nText Mode")
    print("Type 'exit' to return to menu")

    while True:
        text = input("\nEnter text: ")

        if text.lower() == "exit":
            break

        speak(text)


def main():

    while True:
        print("\n===== ROBO SPEAKER =====")
        print("1. Speak Text")
        print("2. Read PDF")
        print("3. Settings")
        print("4. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            text_mode()

        elif choice == "2":
            read_pdf()

        elif choice == "3":
            settings_menu()

        elif choice == "4":
            speak("Bye Bye Friend")

            print("Goodbye!")
            break

        else:
            print("Invalid Choice")


if __name__ == "__main__":
    main()
