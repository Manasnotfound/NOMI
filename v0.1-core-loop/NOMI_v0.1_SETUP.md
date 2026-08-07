# NOMI v0.1 — Setup Guide
**Goal:** Press a button → NOMI takes a photo, records your question, sends both to Claude, and speaks the answer back.

---

## 1. Hardware Checklist
- Raspberry Pi (any model with GPIO — Pi 4/5 recommended for speed)
- Camera: Pi Camera Module (via ribbon cable) **or** any USB webcam
- Microphone: USB mic (easiest — avoids audio driver headaches)
- Speaker: 3.5mm jack speaker or USB speaker
- Push button wired to a GPIO pin (e.g. GPIO17) and ground

If your setup differs (e.g. no button yet, testing with keyboard Enter instead), the script below has a fallback — see the `USE_BUTTON` flag.

---

## 2. OS-Level Setup

Open a terminal on the Pi and run:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv portaudio19-dev libatlas-base-dev espeak ffmpeg
```

If using the Pi Camera Module (not USB webcam), also enable it:
```bash
sudo raspi-config
# Interface Options -> Camera -> Enable -> Reboot
```

---

## 3. Python Environment

```bash
mkdir ~/nomi && cd ~/nomi
python3 -m venv venv
source venv/bin/activate
```

Save this as `requirements.txt`:
```
anthropic
sounddevice
scipy
opencv-python
RPi.GPIO
pyttsx3
```

Then:
```bash
pip install -r requirements.txt
```

> **Note on camera library:** if you're using the Pi Camera Module (not USB), also run `pip install picamera2` — some Pi OS versions ship it system-wide already, so try `import picamera2` first before installing.

---

## 4. API Key

Get an Anthropic API key from [console.anthropic.com](https://console.anthropic.com), then set it as an environment variable so it's never hardcoded in your script:

```bash
echo 'export ANTHROPIC_API_KEY="your-key-here"' >> ~/.bashrc
source ~/.bashrc
```

---

## 5. Run It

```bash
cd ~/nomi
source venv/bin/activate
python3 main.py
```

Press the button (or hit Enter, if `USE_BUTTON = False`), ask your question out loud, and NOMI will look, listen, think, and speak.

---

## 6. What's Deliberately Simple in v0.1 (upgrade later)
- **TTS is `pyttsx3`** (robotic, offline, zero setup) — swap for **Piper TTS** later for a natural voice, matches your privacy-first philosophy since it also runs offline.
- **No wake word yet** — button press only. Wake-word detection (e.g. Porcupine) is a v0.2+ nice-to-have.
- **No memory yet** — every question is a fresh conversation. That's Version 0.2.
- **STT happens via the Claude API itself is NOT used for audio** — Claude's API doesn't take raw audio input, so we record audio, and for v0.1 we're keeping it simple by typing the question via terminal input if you don't yet have local speech-to-text installed. See the `TRANSCRIBE_LOCALLY` flag in the script — flip it on once you install `vosk` for real voice questions.
