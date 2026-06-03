# creating a robo speaker using python which will speak the text given by the user,
# and will continue to speak until the user types "exit" to stop the program.
# The program will also set the properties of the speech such as speed and volume.

import pyttsx3
import os

print("Welcome to Robo Speaker!")

while True:
    text = input("Enter text (type 'exit' to quit): ")

    if text.lower() == "exit":
        os.system(
            'powershell -Command "Add-Type -AssemblyName System.Speech; '
            "(New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak('Bye Bye Friend!')\""
        )
        break

    safe_text = text.replace("'", "''")

    command = (
        'powershell -Command "Add-Type -AssemblyName System.Speech; '
        f"(New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak('{safe_text}')\""
    )

    os.system(command)
