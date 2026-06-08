import asyncio
import os
import tempfile
import threading

import edge_tts
import pygame
import win32com.client

from utils import load_json

is_paused = False
is_stopped = False
audio_thread = None
playback_active = False

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

    if not pygame.mixer.get_init():
        pygame.mixer.init()

    pygame.mixer.music.load(temp_path)

    global playback_active
    playback_active = True

    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy() or is_paused:
        if is_stopped:
            pygame.mixer.music.stop()
            break

        await asyncio.sleep(0.1)

    playback_active = False

    pygame.mixer.music.unload()

    try:
        os.remove(temp_path)
    except Exception:
        pass


def run_edge_thread(text):

    try:
        asyncio.run(edge_speak_async(text))

    except RuntimeError:
        loop = asyncio.new_event_loop()

        asyncio.set_event_loop(loop)

        loop.run_until_complete(edge_speak_async(text))

        loop.close()


def speak_edge(text):

    global audio_thread
    global is_stopped

    is_stopped = False

    if audio_thread and audio_thread.is_alive():
        stop_audio()

    audio_thread = threading.Thread(target=run_edge_thread, args=(text,), daemon=True)

    audio_thread.start()


def pause_audio():

    global is_paused

    if playback_active:
        pygame.mixer.music.pause()

        is_paused = True

        print("Paused")


def resume_audio():

    global is_paused

    if playback_active and is_paused:
        pygame.mixer.music.unpause()

        is_paused = False

        print("Resumed")


def stop_audio():

    global playback_active
    global is_paused
    global is_stopped

    is_stopped = True

    try:
        pygame.mixer.music.stop()

    except:
        pass

    playback_active = False

    is_paused = False

    print("Stopped")


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


def speak_sync(text):
    settings = load_settings()

    engine = settings["voice_engine"]

    if engine == "edge":
        speak_edge(text)
    else:
        speak_sapi(text)
