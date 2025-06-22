import speech_recognition as sr
import pyttsx3
import math
import re

# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
tts = pyttsx3.init()

def speak(text):
    """Convert text to speech"""
    tts.say(text)
    tts.runAndWait()

def listen():
    """Capture voice input"""
    with sr.Microphone() as source:
        print("Speak now...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return None
    except sr.RequestError as e:
        speak(f"Request error from Google Speech Recognition service; {e}")
        return None

def process_command(command):
    """Map spoken words to Python syntax and evaluate"""
    if command is None:
        return

    print(f"Raw command before replacement: {command}")

    # Replace spoken words with Python operators — longer phrases first
    command = command.replace("divided by", "/")
    command = command.replace("plus", "+")
    command = command.replace("minus", "-")
    command = command.replace("multiply", "*")
    command = command.replace("multiplied by", "*")
    command = command.replace("times", "*")
    command = command.replace("divide", "/")
    command = command.replace("x", "*")

    # Replace 'square root of' and 'square root' with math.sqrt(
    command = command.replace("square root of ", "math.sqrt(")
    command = command.replace("square root ", "math.sqrt(")

    # Use regex to find math.sqrt(number) without closing ) and close it
    pattern = r"math\.sqrt\((\d+)"
    command = re.sub(pattern, r"math.sqrt(\1)", command)

    # Check for incomplete math.sqrt(
    if "math.sqrt(" in command and not re.search(r"math\.sqrt\(\d+\)", command):
        speak("Please say a number after square root.")
        print("No number after square root. Command skipped.")
        return

    print(f"Processed command for eval: {command}")

    try:
        result = eval(command, {"math": math})
        print(f"Result: {result}")
        speak(f"The result is {result}")
    except Exception as e:
        print(f"Error: {e}")
        speak("Sorry, I couldn't understand or run that command.")

# Main program loop
while True:
    command = listen()
    if command:
        if "exit" in command or "stop" in command:
            speak("Goodbye, Naufal.")
            break
        process_command(command)
