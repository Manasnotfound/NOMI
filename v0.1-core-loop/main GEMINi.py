
import time

import cv2
from google import genai
from google.genai import types
import pyttsx3


USE_BUTTON = False          # True once your GPIO button is wired up; False = press Enter instead
TRANSCRIBE_LOCALLY = False  # True once you install `vosk` for real voice-to-text
CAMERA_INDEX = 0            # 0 = default webcam. For Pi Camera Module, see picamera2 branch below
USE_PI_CAMERA_MODULE = False  

if USE_BUTTON:
    import RPi.GPIO as GPIO
    BUTTON_PIN = 17
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

if TRANSCRIBE_LOCALLY:
    import sounddevice as sd
    from scipy.io.wavfile import write as wav_write
    import vosk
    import json


client = genai.Client()  # reads GEMINI_API_KEY from environment
tts_engine = pyttsx3.init()
GEMINI_MODEL = "gemini-2.5-flash"  # fast + cheap, good for a conversational companion


def speak(text: str):
    print(f"NOMI: {text}")
    tts_engine.say(text)
    tts_engine.runAndWait()


def wait_for_trigger():
    """Blocks until the button is pressed (or Enter is hit in dev mode)."""
    if USE_BUTTON:
        print("Waiting for button press...")
        GPIO.wait_for_edge(BUTTON_PIN, GPIO.FALLING)
    else:
        input("Press Enter to ask NOMI a question...")


def capture_image() -> str:
    """Captures a photo and returns the path to the saved JPEG."""
    image_path = "capture.jpg"

    if USE_PI_CAMERA_MODULE:
        from picamera2 import Picamera2
        picam2 = Picamera2()
        picam2.start_and_capture_file(image_path)
        picam2.stop()
    else:
        cam = cv2.VideoCapture(CAMERA_INDEX)
        time.sleep(0.3)  # let the camera sensor warm up / auto-expose
        ret, frame = cam.read()
        cam.release()
        if not ret:
            raise RuntimeError("Camera capture failed - check CAMERA_INDEX / connection")
        cv2.imwrite(image_path, frame)

    return image_path


def get_question() -> str:
    """Returns the user's question as text.
    v0.1 default: type it in. Flip TRANSCRIBE_LOCALLY on once vosk is installed
    for real voice input.
    """
    if not TRANSCRIBE_LOCALLY:
        return input("What do you want to ask NOMI? ")


    duration = 4  # seconds to record
    fs = 16000
    print("Listening...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype="int16")
    sd.wait()
    wav_write("question.wav", fs, recording)

    model = vosk.Model("model")
    rec = vosk.KaldiRecognizer(model, fs)
    with open("question.wav", "rb") as f:
        data = f.read()
    rec.AcceptWaveform(data)
    result = json.loads(rec.Result())
    return result.get("text", "")


def ask_gemini(image_path: str, question: str) -> str:
    """Sends the image + question to Gemini and returns the answer text."""
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=[
            types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
            question,
        ],
        config=types.GenerateContentConfig(
            system_instruction=(
                "You are NOMI, a curious, friendly pocket companion. "
                "Keep answers short (2-3 sentences), warm, and conversational - "
                "you're speaking out loud, not writing an essay."
            ),
            max_output_tokens=300,
        ),
    )
    return response.text


def main():
    print("NOMI v0.1 is awake. (Ctrl+C to stop)")
    try:
        while True:
            wait_for_trigger()
            print("Looking and thinking...")

            image_path = capture_image()
            question = get_question()

            if not question.strip():
                speak("I didn't catch that, try again?")
                continue

            answer = ask_gemini(image_path, question)
            speak(answer)

    except KeyboardInterrupt:
        print("\nNOMI is going to sleep. Bye!")
    finally:
        if USE_BUTTON:
            GPIO.cleanup()


if __name__ == "__main__":
    main()
