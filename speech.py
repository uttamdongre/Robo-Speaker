import win32com.client
from utils import load_json


speaker = win32com.client.Dispatch("SAPI.SpVoice")


def load_settings():

    settings = load_json("settings.json")

    rate = settings.get("speech_rate", 0)

    voice_index = settings.get("voice_index", 0)

    speaker.Rate = rate

    voices = speaker.GetVoices()

    if voice_index < voices.Count:
        speaker.Voice = voices.Item(voice_index)


def speak(text):
    if not text:
        return

    load_settings()

    print(f"\nSpeaking: {text[:60]}...")
    speaker.Speak(text)


def get_voices():
    voices = speaker.GetVoices()

    for i in range(voices.Count):
        print(f"{i}. {voices.Item(i).GetDescription()}")
