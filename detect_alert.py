import os, time, requests
from ultralytics import YOLO

# --- config ---
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
COOLDOWN = 60          # seconds between alerts for the same object
CONFIDENCE = 0.7       # ignore weak detections

model = YOLO("models/yolo11n.pt")
last_alert = {}        # tracks when we last alerted per object type


def send(text, image_path=None):
    """Send a Telegram message, optionally with a photo."""
    try:
        if image_path:
            url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
            with open(image_path, "rb") as photo:
                requests.post(url, data={"chat_id": CHAT_ID, "caption": text},
                              files={"photo": photo}, timeout=10)
        else:
            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
            requests.post(url, data={"chat_id": CHAT_ID, "text": text}, timeout=10)
    except Exception as e:
        print(f"Telegram error: {e}")


send("🟢 Detector started")
print("Running. Ctrl+C to stop.")

try:
    for r in model.predict(source=0, stream=True, conf=CONFIDENCE, verbose=False):
        now = time.time()

        # what did we see in this frame?
        seen = {model.names[int(c)] for c in r.boxes.cls}

        for label in seen:
            # only alert if we haven't alerted for this object recently
            if now - last_alert.get(label, 0) > COOLDOWN:
                last_alert[label] = now
                path = "alert.jpg"
                r.save(path)                       # annotated frame with boxes
                send(f"👀 Detected: {label}", path)
                print(f"ALERT: {label}")
except KeyboardInterrupt:
    send("🔴 Detector stopped")
    print("\nStopped.")
