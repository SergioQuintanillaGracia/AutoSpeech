# IMPORTANT: For all program functionalities to work, you'll need to
# install the following packages:
# xdotool: Close windows.


import sounddevice
import speech_recognition as sr
import subprocess
import os

comm_firefox = (("open", "start"), ("firefox", "browser"))
comm_close_curr = (("close", "exit", "kill"), ("current", "this", "the"), ("window", "program", "process"))
comm_maximize_window = (("maximize"), ("window", "program"))


def recognize_speech_from_mic(recognizer, microphone):
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        # Listen for a single phrase.
        audio = recognizer.listen(source)

    try:
        return recognizer.recognize_google(audio)
    except sr.RequestError:
        return "API unavailable"
    except sr.UnknownValueError:
        return "Unable to recognize speech"


def get_active_window_id():
    # Get the active window ID:
    return subprocess.run(["xdotool", "getactivewindow"], capture_output=True, text=True).stdout.strip()


def detectCommand(command, comm_list):
    command_lower = command.lower()

    for subcomm_list in comm_list:
        if not any(comm in command_lower for comm in subcomm_list):
            return False
        
    return True


def open_application(command):
    if detectCommand(command, comm_firefox):
        subprocess.Popen(["firefox"])
    
    if detectCommand(command, comm_close_curr):
        subprocess.run(["xdotool", "key", "alt+F4"])
    
    if detectCommand(command, comm_maximize_window):
        subprocess.run(["xdotool", "key", "super+enter"])


recognizer = sr.Recognizer()
microphone = sr.Microphone()

open_application("maximize window")

while True:
    print("Listening for command...")
    command = recognize_speech_from_mic(recognizer, microphone)
    print("You said:", command)

    if command:
        open_application(command)
