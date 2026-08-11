from email.mime import text
from pdb import main
import speech_recognition as sr
import pyttsx3

""" def speech_to_text():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer = sr.Recognizer()
        audio = recognizer.listen(source)   
        text = recognizer.recognize_google(audio)
        return text """

def command_input():
    text = input("Enter your command: ")
    pyttsx3.speak(f"the following command has been received: {text}")
    if "Nomi" in text:
        print("Nomi is awake")
    text = text.split()
    print(text)
                
if __name__ == "__main__":
    command_input()