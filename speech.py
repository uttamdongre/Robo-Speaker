import asyncio
import os
import tempfile

import edge_tts
import pygame
import win32com.client

from utils import load_json


# -------------------------
# SAPI FALLBACK
# -------------------------

speaker = win32com.client.Dispatch("SAPI.SpVoice")


# -------------------------
# SETTINGS
# -------------------------


def load_settings():

    settings = load_json("settings.json")

    return {
        "voice_engine": settings.get("voice_engine", "sapi"),
        "voice_name": settings.get("voice_name", "en-US-AriaNeural"),
        "speech_rate": settings.get("speech_rate", 0),
    }


# -------------------------
# SAPI VOICE
# -------------------------


def speak_sapi(text):

    if not text.strip():
        return

    settings = load_settings()

    speaker.Rate = settings["speech_rate"]

    speaker.Speak(text)


# -------------------------
# EDGE TTS
# -------------------------


async def edge_speak_async(text):

    settings = load_settings()

    voice = settings["voice_name"]

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")

    temp_path = temp_file.name

    temp_file.close()

    communicate = edge_tts.Communicate(text=text, voice=voice)

    await communicate.save(temp_path)

    pygame.mixer.init()

    pygame.mixer.music.load(temp_path)

    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        await asyncio.sleep(0.1)

    pygame.mixer.music.unload()

    try:
        os.remove(temp_path)
    except:
        pass


def speak_edge(text):
    try:
        asyncio.run(edge_speak_async(text))
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(edge_speak_async(text))
        loop.close()


# -------------------------
# MAIN SPEAK
# -------------------------


def speak(text):

    if not text or not text.strip():
        return

    settings = load_settings()

    engine = settings["voice_engine"]

    try:
        if engine == "edge":
            speak_edge(text)

        else:
            speak_sapi(text)

    except Exception as e:
        print(f"\nNeural voice failed: {e}")

        print("Switching to SAPI...")

        speak_sapi(text)
