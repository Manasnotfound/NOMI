from email.mime import text
import os
import speech_recognition as sr
import time
import cv2

def speech_to_text():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer = sr.Recognizer()
        audio = recognizer.listen(source)   
        text = recognizer.recognize_google(audio)
        print(text)
    speech_to_text()
 
def input_command():
    command = input("Press Enter to ask NOMI a question...").casefold()
    if command == "nomi capture":
        print("NOMI Capture command received, capturing image...")
        return True
    return False

if __name__ == "__main__":
    speech_to_text()