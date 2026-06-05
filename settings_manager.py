from utils import load_json, save_json
import win32com.client


SETTINGS_FILE = "settings.json"


def load_settings():
    return load_json(SETTINGS_FILE)


def save_settings(settings):
    save_json(SETTINGS_FILE, settings)


def change_speed():

    settings = load_settings()

    print("\nSpeech Speed")
    print("1. Slow")
    print("2. Normal")
    print("3. Fast")

    choice = input("\nChoose: ")

    if choice == "1":
        settings["speech_rate"] = -2

    elif choice == "2":
        settings["speech_rate"] = 0

    elif choice == "3":
        settings["speech_rate"] = 2

    else:
        print("Invalid Choice")
        return

    save_settings(settings)

    print("Speech speed updated")


def change_voice():

    settings = load_settings()

    speaker = win32com.client.Dispatch("SAPI.SpVoice")

    voices = speaker.GetVoices()

    print("\nAvailable Voices\n")

    for i in range(voices.Count):
        print(f"{i}. {voices.Item(i).GetDescription()}")

    try:
        choice = int(input("\nSelect Voice Number: "))

        if 0 <= choice < voices.Count:
            settings["voice_index"] = choice

            save_settings(settings)

            print("Voice updated")

        else:
            print("Invalid Voice Number")

    except:
        print("Invalid Input")


def show_settings():

    settings = load_settings()

    rate = settings.get("speech_rate", 0)

    voice_index = settings.get("voice_index", 0)

    speaker = win32com.client.Dispatch("SAPI.SpVoice")

    voices = speaker.GetVoices()

    voice_name = "Unknown"

    if voice_index < voices.Count:
        voice_name = voices.Item(voice_index).GetDescription()

    speed_name = {-2: "Slow", 0: "Normal", 2: "Fast"}.get(rate, str(rate))

    print("\nCurrent Settings\n")

    print(f"Voice : {voice_name}")
    print(f"Speed : {speed_name}")


def settings_menu():

    while True:
        print("\n===== SETTINGS =====")
        print("1. Change Speech Speed")
        print("2. Change Voice")
        print("3. Show Current Settings")
        print("4. Back")

        choice = input("\nChoose: ")

        if choice == "1":
            change_speed()

        elif choice == "2":
            change_voice()

        elif choice == "3":
            show_settings()

        elif choice == "4":
            break

        else:
            print("Invalid Choice")
