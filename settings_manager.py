from utils import load_json, save_json
import win32com.client

EDGE_VOICES = {
    "1": ("Aria Female", "en-US-AriaNeural"),
    "2": ("Jenny Female", "en-US-JennyNeural"),
    "3": ("Guy Male", "en-US-GuyNeural"),
    "4": ("Davis Male", "en-US-DavisNeural"),
    "5": ("Sonia Female", "en-GB-SoniaNeural"),
    "6": ("Ryan Male", "en-GB-RyanNeural"),
}

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


def change_neural_voice():

    settings = load_settings()

    print("\nAvailable Neural Voices\n")

    for key, (name, voice) in EDGE_VOICES.items():
        print(f"{key}. {name}")

    choice = input("\nChoose Voice: ")

    if choice in EDGE_VOICES:
        settings["voice_name"] = EDGE_VOICES[choice][1]

        save_settings(settings)

        print("Neural voice updated")

    else:
        print("Invalid Choice")


def change_voice_engine():

    settings = load_settings()

    print("\nVoice Engine")

    print("1. Windows SAPI")
    print("2. Edge Neural")

    choice = input("\nChoose: ")

    if choice == "1":
        settings["voice_engine"] = "sapi"

    elif choice == "2":
        settings["voice_engine"] = "edge"

    else:
        print("Invalid Choice")
        return

    save_settings(settings)

    print("Voice engine updated")


def change_voice_engine():

    settings = load_settings()

    print("\nVoice Engine")
    print("1. Windows SAPI")
    print("2. Edge Neural Voice")

    choice = input("\nChoose: ")

    if choice == "1":
        settings["voice_engine"] = "sapi"

    elif choice == "2":
        settings["voice_engine"] = "edge"

        settings["voice_name"] = "en-US-AriaNeural"

    else:
        print("Invalid Choice")
        return

    save_settings(settings)

    print("Voice engine updated")


def show_settings():

    settings = load_settings()

    print("\nCurrent Settings\n")

    print(f"Voice Engine : {settings.get('voice_engine', 'sapi')}")

    print(f"Neural Voice : {settings.get('voice_name', 'N/A')}")

    rate = settings.get("speech_rate", 0)

    speed_name = {-2: "Slow", 0: "Normal", 2: "Fast"}.get(rate, str(rate))

    print(f"Speed : {speed_name}")


def settings_menu():

    while True:
        print("\n===== SETTINGS =====")

        print("1. Change Speech Speed")
        print("2. Change Voice Engine")
        print("3. Change Neural Voice")
        print("4. Show Current Settings")
        print("5. Back")

        choice = input("\nChoose: ")

        if choice == "1":
            change_speed()

        elif choice == "2":
            change_voice_engine()

        elif choice == "3":
            change_neural_voice()

        elif choice == "4":
            show_settings()

        elif choice == "5":
            break

        else:
            print("Invalid Choice")
