import os, sys, time, threading, requests
import cv2
from ultralytics import YOLO
from describe import describe

# --- config ---
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
COOLDOWN = 10          # seconds between alerts for the same object
CONFIDENCE = 0.7       # ignore weak detections

# Run with "--people" to alert on people only. classes=[0] restricts YOLO to
# COCO class 0 = "person"; classes=None (the default) reports all 80 objects.
PEOPLE_ONLY = "--people" in sys.argv
CLASSES = [0] if PEOPLE_ONLY else None

# Run with "--describe" to caption alerts with a one-sentence scene description
# from Claude's vision model (describe.py). Off by default — this is the only
# mode that sends a frame off the device, so it stays opt-in.
DESCRIBE = "--describe" in sys.argv


# Run with "--model PATH" to use a custom model (e.g. models/best.pt for Funkos).
def arg_value(flag, default):
    if flag in sys.argv:
        i = sys.argv.index(flag)
        if i + 1 < len(sys.argv):
            return sys.argv[i + 1]
    return default


MODEL = arg_value("--model", "models/yolo11n.pt")
model = YOLO(MODEL)
last_alert = {}        # tracks when we last alerted per object type


def send(text, image=None):
    """Send a Telegram message. `image` may be a file path (str) or JPEG bytes."""
    try:
        if image is None:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                          data={"chat_id": CHAT_ID, "text": text}, timeout=10)
            return
        url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
        data = {"chat_id": CHAT_ID, "caption": text}
        if isinstance(image, (bytes, bytearray)):
            requests.post(url, data=data,
                          files={"photo": ("alert.jpg", image)}, timeout=10)
        else:
            with open(image, "rb") as photo:
                requests.post(url, data=data, files={"photo": photo}, timeout=10)
    except Exception as e:
        print(f"Telegram error: {e}")


def deliver(label, annotated_bytes, clean_bytes):
    """The slow path, run in a background thread so the detection loop never
    blocks: describe the CLEAN frame, then send the ANNOTATED photo. On any
    describe failure the caption falls back to the plain label."""
    caption = f"👀 Detected: {label}"
    if clean_bytes:
        sentence = describe(clean_bytes)
        if sentence:
            caption = f"👀 {sentence}"
    send(caption, annotated_bytes)


send("🟢 Detector started (people only)" if PEOPLE_ONLY else "🟢 Detector started")
print("Running. Ctrl+C to stop.")

try:
    for r in model.predict(source=0, stream=True, conf=CONFIDENCE,
                           classes=CLASSES, verbose=False):
        now = time.time()

        # what did we see in this frame?
        seen = {model.names[int(c)] for c in r.boxes.cls}

        for label in seen:
            # only alert if we haven't alerted for this object recently
            if now - last_alert.get(label, 0) > COOLDOWN:
                last_alert[label] = now
                r.save("alert.jpg")                # on-disk snapshot (annotated)

                if DESCRIBE:
                    # Hand the slow work to a background thread. Snapshot BOTH
                    # frames to bytes now, so the thread can't race the next
                    # alert overwriting the shared file. The loop keeps pulling
                    # frames — YOLO never goes blind during the ~1.6s API call.
                    ok, clean = cv2.imencode(".jpg", r.orig_img)    # clean → API
                    with open("alert.jpg", "rb") as f:
                        annotated = f.read()                        # annotated → Telegram
                    threading.Thread(
                        target=deliver,
                        args=(label, annotated, clean.tobytes() if ok else None),
                        daemon=True,
                    ).start()
                else:
                    send(f"👀 Detected: {label}", "alert.jpg")
                print(f"ALERT: {label}")
except KeyboardInterrupt:
    send("🔴 Detector stopped")
    print("\nStopped.")
