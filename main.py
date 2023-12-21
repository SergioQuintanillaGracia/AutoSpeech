import sounddevice
import speech_recognition as sr
import subprocess
import os

def recognize_speech_from_mic(recognizer, microphone):
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        return recognizer.recognize_google(audio)
    except sr.RequestError:
        return "API unavailable"
    except sr.UnknownValueError:
        return "Unable to recognize speech"

def open_application(command):
    if "open firefox" in command.lower():
        subprocess.Popen(["firefox"])
    # Add more commands and applications here

recognizer = sr.Recognizer()
microphone = sr.Microphone()

while True:
    print("Listening for command...")
    command = recognize_speech_from_mic(recognizer, microphone)
    print("You said:", command)

    if command:
        open_application(command)
