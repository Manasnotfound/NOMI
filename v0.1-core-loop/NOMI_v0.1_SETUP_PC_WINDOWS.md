# NOMI v0.1 — Windows PC Setup (Testing Before Pi)

Same `main.py` you already have — no code changes needed. The config flags (`USE_BUTTON = False`, `USE_PI_CAMERA_MODULE = False`) already default to "PC mode": Enter-key trigger, USB webcam via OpenCV. This lets you debug the whole software loop before touching the Pi at all.

---

## 1. Install Python (if not already installed)
Download from [python.org/downloads](https://python.org/downloads) — **check "Add Python to PATH"** during install. Verify in Command Prompt:
```
python --version
```

---

## 2. Set Up the Project

Open Command Prompt (or PowerShell) in your project folder:
```
cd path\to\nomi
python -m venv venv
venv\Scripts\activate
```
You'll know it worked when your prompt shows `(venv)` at the start.

---

## 3. Install Dependencies

Create `requirements.txt` with these (note: **no** `RPi.GPIO`, **no** `picamera2` — those are Pi-only and would fail to install on Windows):
```
anthropic
opencv-python
pyttsx3
```

Then:
```
pip install -r requirements.txt
```

`pyttsx3` uses Windows' built-in SAPI5 voices, so no extra audio drivers needed for TTS.

---

## 4. Set Your API Key

In Command Prompt:
```
setx ANTHROPIC_API_KEY "your-key-here"
```
**Close and reopen** Command Prompt after this (setx needs a fresh session to take effect). Verify with:
```
echo %ANTHROPIC_API_KEY%
```

---

## 5. Check Your Webcam Index

Windows sometimes assigns webcam index `1` instead of `0` if you have a built-in laptop cam too. Quick test — run this in Python to confirm:
```python
import cv2
cam = cv2.VideoCapture(0)  # try 0, then 1 if this fails
ret, frame = cam.read()
print("Camera working:", ret)
cam.release()
```
If `ret` is `False`, change `CAMERA_INDEX = 1` (or higher) in `main.py`.

---

## 6. Run It

```
venv\Scripts\activate
python main.py
```

Hit Enter, type your question when prompted, and NOMI should look through your webcam and speak an answer via Windows TTS.

---

## 7. USB Mic — Not Wired In Yet

Right now `main.py` uses **typed questions**, not live mic input — that's intentional for v0.1 so you can debug the vision+API+speech pipeline in isolation first. Once that's working end-to-end, say the word and we'll wire in real voice input using your USB mic (via `sounddevice` + `vosk`, both work fine on Windows too) — same flag flip (`TRANSCRIBE_LOCALLY = True`) as planned for the Pi.

---

## Later: Moving to the Pi
Nothing here is wasted — same `main.py`, same API logic. When you move to the Pi, you'll just flip `USE_PI_CAMERA_MODULE` (if using ribbon-cable camera) and `USE_BUTTON` back on, and follow the earlier Pi setup guide for the Linux-specific installs.
